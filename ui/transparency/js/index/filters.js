/* 
=====================================
HOW TO ADD A NEW FILTER
=====================================
init_dashboards()
    Design the dashboard of the filter
    The user interact with it to set the value for the filter
    Store it in this.dashboard
        html: the actual dashboard
        setState: a funtion to set css styles if filter is active
        description: the user will see this
    
bindEvents()
    Bind your event of the dashboard

init_options()
    Initialize the value to false.

init_captions()
    Design the caption and create an update function
*/
$(function () {
    var filters = {
        filters: {}, // goes to backend
        templates: {}, // {name: {template: .mustache, render: function()},...}
        options: {}, // dropdown menu
        dashboards: {}, // html strings e.g. {type: "...",...}
        current:[], // current editable filters [{name:, value:}, ...]
        captions: {}, 
        lastUpdate: 0,
        pending: null,
        first: true,
        delay: 150,

        init: async function() {
            await this.init_templates();
            this.init_filters();
            this.init_options();
            await this.init_dashboards();
            this.init_captions();
            this.cacheDom();
            this.filtersRender();
            this.bindEvents();
            this.request();
        },

        cacheDom: function() {
            this.$topic = $("#topic");
            this.$tbody = $("#resultsTable tbody");
            this.$filters = $(".filters .columns");
            this.$modal = $(".modal.modal__bg#filters");
        },

        init_dashboards: async function() {
            this.dashboards.task = {html: "", setState: this.taskSetState.bind(this), description: 'Filter model cards by task.'};
            this.dashboards.type = {html: "", setState: this.typeSetState.bind(this), description: 'Filter model cards by model architecture or algorithm.'};
            this.dashboards.info = {html: "", setState: this.infoSetState.bind(this), description: 'Show only model cards based on how complete their information is.'};
            this.dashboards.params = {html: "", setState: this.paramsSetState.bind(this), description: 'Filter model cards by number of parameters.'};
            this.dashboards.energy = {html: "", setState: this.energySetState.bind(this), description: 'Filter model cards by energy consumption.'};
            this.getTaskDashboard().then(function (html) { this.dashboards.task.html = html; }.bind(this));
            this.getTypeDashboard().then(function (html) { this.dashboards.type.html = html; }.bind(this));
            this.dashboards.info.html = this.getInfoDashboard();
            this.getParamsDashboard().then(function(html) { this.dashboards.params.html=html }.bind(this));
            this.getEnergyDashboard().then(function(html) { this.dashboards.energy.html=html }.bind(this));
        },

        init_captions: function() {
            this.captions.task = {update: this.updateTaskCaption.bind(this)};
            this.captions.type = {update: this.updateTypeCaption.bind(this)};
            this.captions.info = {update: this.updateInfoCaption.bind(this)};
            this.captions.params = {update: this.updateParamsCaption.bind(this)};
            this.captions.energy = {update: this.updateEnergyCaption.bind(this)};
        },

        init_options: function() {
            this.options.task = {active: false};
            this.options.type = {active: false};
            this.options.info = {active: false};
            this.options.params = {active: false};
            this.options.energy = {active: false};
        },

        init_templates: async function () {
            this.templates.cardRow = {template: "", render: this.cardRowRender.bind(this), path: "templates/index/cardRow.mustache"};
            this.templates.modal = {template: "", render: this.modalRender.bind(this), path: "templates/index/filtersModal.mustache"};
            this.templates.editModal = {template: "", render: this.EditModalRender.bind(this), path: "templates/index/filtersModal.mustache"};
            await this.loadTemplates(this.templates);
        },

        init_filters: function() {
            this.filters.query = '';
        },

        bindEvents: function() { 
            this.$filters.on('click', '#new-filter', this.newFilter.bind(this));
            this.$filters.on('click', '.remove-filter', this.removeFilter.bind(this));
            this.$filters.on('click', '#edit-filter', this.editFilter.bind(this));
            this.$modal.on('change', '#filter-select', this.dashboardRender.bind(this));
            this.$topic.on("keyup", this.topicCallback.bind(this));
            this.$modal.on('click', '.filter-done', this.done.bind(this));
            this.$modal.on('click', '.filter-cancel', this.cancel.bind(this));
            this.$modal.on('click', '.filter-dashboard[data-filter="task"]', this.filterTask.bind(this));
            this.$modal.on('click', '.filter-dashboard[data-filter="type"]', this.filterType.bind(this));
            this.$modal.on('input', '.filter-dashboard[data-filter="info"] .info-input', this.filterInfo.bind(this));
            this.$modal.on('input', '#paramsFilter input', this.filterParam.bind(this));
            this.$modal.on('input', '#energyFilter input', this.filterEnergy.bind(this));
        },


        ////////////////////////////
        //       Ugly Logic       //
        ////////////////////////////

        updateTaskCaption: function(){
            let value = ''
            this.filters.task.forEach(item => { 
                value += `<span class="captionValue">${noLineBreak(item)}</span> `
            })
            this.captionBuilder('task', value)
        },

        updateTypeCaption: function(){
            let value = ''
            this.filters.type.forEach(item => { 
                value += `<span class="captionValue">${noLineBreak(item)}</span> `
            })
            this.captionBuilder('type', value)
        },

        updateInfoCaption: function(){
            const value = `<span class="captionValue">${this.filters.info}&nbsp;%</span>`
            this.captionBuilder('info', value);
        },
        updateParamsCaption: function(){
            let inner;
            if (this.filters.params[0] === '<1B' && this.filters.params[1] === '>500B') {
                inner = 'All';
            }
            else if (this.filters.params[0] === '<1B'){
                inner = `≤ ${this.filters.params[1]}`;
            } 
            else if (this.filters.params[1] === '>500B'){
                inner = `≥ ${this.filters.params[0]}`;
            }
            else{
                inner= `${this.filters.params[0]} - ${this.filters.params[1]}`;
            }
            const value = `<span class="captionValue">${inner}</span>`;
            this.captionBuilder('params', value);
        },
        updateEnergyCaption: function(){
            let inner;
            if (this.filters.energy[0] === '<0.1cll' && this.filters.energy[1] === '>500cll') {
                inner = 'All';
            }
            else if (this.filters.energy[0] === '<0.1cll'){
                inner = `≤ ${this.filters.energy[1]}`;
            } 
            else if (this.filters.energy[1] === '>500cll'){
                inner = `≥ ${this.filters.energy[0]}`;
            }
            else{
                inner= `${this.filters.energy[0]} - ${this.filters.energy[1]}`;
            }
            const value = `<span class="captionValue">${inner}</span>`;
            this.captionBuilder('energy', value);
        },
        captionBuilder: function(filter, value){
            const icon = '<i class="fa-solid fa-pencil"></i>'
            const $caption = $('<div>').html(`${icon}&nbsp;${capitalizeFirstLetter(filter)}:  ${value}`);
            const $cancel = $('<div>').html(`<span class="remove-filter">X</span>`);
            this.$filters.find(`[data-filter="${filter}"]`).empty().append($caption).append($cancel);
        },
        taskSetState: function() {
            const index = this.current.findIndex(item => item.name === "task");
            this.current[index].value.forEach(function(task){
                this.$modal.find('[data-filter="' + task + '"]').addClass("active");
            }.bind(this));
            // update optgroups
            $('.filter-optgroup').each(function () {
                const options = $(this).nextUntil('.filter-optgroup', '.filter-option');
                if (options.filter('.active').length === options.length) {
                    $(this).addClass('active');
                } else {
                    $(this).removeClass('active');
                }
            });
        },
        typeSetState: function() {
            const index = this.current.findIndex(item => item.name === "type");
            this.current[index].value.forEach(function(type){
                this.$modal.find('[data-filter="' + type + '"]').addClass("active");
            }.bind(this));
            // update optgroups
            $('.filter-optgroup').each(function () {
                const options = $(this).nextUntil('.filter-optgroup', '.filter-option');
                if (options.filter('.active').length === options.length) {
                    $(this).addClass('active');
                } else {
                    $(this).removeClass('active');
                }
            });
        },
        infoSetState: function() {
            const index = this.current.findIndex(item => item.name === "info");
            $('.info-input')
                .val(this.current[index].value)
                .css('background', 'linear-gradient(90deg, var(--text-primary) '+ this.current[index].value + '%, var(--bg-tertiary) '+this.current[index].value+'%)');
            $('.info-value').text(this.current[index].value);
            
        },
        paramsSetState: function() {
            const $params = $('#paramsFilter');
            const validValues = ['<1B', '3B', '6B', '9B', '12B', '24B', '32B', '64B', '128B', '256B', '>500B'];
            const index = this.current.findIndex(item => item.name === "params");
            let minVal = validValues.findIndex(item => item === this.current[index].value[0]);
            let maxVal = validValues.findIndex(item => item === this.current[index].value[1]);
            $params.find('#min').val(minVal);
            $params.find('#max').val(maxVal);
            $params.find('#fill').css({left: minVal*10+'%', width: (maxVal-minVal)*10+'%'});
            $params.find('.label').each((i,el)=> {el.classList.toggle('active', i===minVal || i===maxVal)})
        },
        energySetState: function() {
            const $energy = $('#energyFilter');
            const validValues = ['<0.1cll', '0.5cll', '1cll', '5cll', '10cll', '20cll', '40cll', '80cll', '160cll', '320cll', '>500cll'];
            const index = this.current.findIndex(item => item.name === "energy");
            console.log(this.current);
            let minVal = validValues.findIndex(item => item === this.current[index].value[0]);
            let maxVal = validValues.findIndex(item => item === this.current[index].value[1]);
            $energy.find('#min').val(minVal);
            $energy.find('#max').val(maxVal);
            $energy.find('#fill').css({left: minVal*10+'%', width: (maxVal-minVal)*10+'%'});
            $energy.find('.label').each((i,el)=> {el.classList.toggle('active', i===minVal || i===maxVal)})
        },
        editFilter: function(e) {
            if ($(e.target).closest('.remove-filter').length) return;
            const filter = $(e.currentTarget).attr('data-filter');
            this.current.push({name: filter, value: this.filters[filter]});
            this.EditModalRender(filter);
            this.dashboards[filter].setState();
        },
        EditModalRender: function(filter) {
            const dashboard = this.dashboards[filter].html;
            this.$modal.addClass('modal--active').html(this.templates.editModal.template);
            $('.filter-title h1').text('Edit Filter')
            $filterdashboard = $(".filter-dashboard");
            $filterdashboard
                .html(dashboard)
                .attr('data-filter', filter)
                .css('overflow-y', 'auto');
            $('.dashboard-description').text(capitalizeFirstLetter(filter)+': '+this.dashboards[filter].description);
        },
        filterParam: function (e){
            const index = this.current.findIndex(item => item.name === "params");
            const validValues = ['<1B', '3B', '6B', '9B', '12B', '24B', '32B', '64B', '128B', '256B', '>500B'];
            const $params = $('#paramsFilter');
            const $min = $params.find('#min');
            const $max = $params.find('#max');
            let minVal = Number($min.val());
            let maxVal = Number($max.val());
            if(e){
                if(e.target===$min[0] && minVal >= maxVal && maxVal !==10 ) $min.val(maxVal-1);
                else if( e.target === $max[0] && maxVal <= minVal && minVal !==0 ) $max.val(minVal+1);
            }
            minVal = Number($min.val());
            maxVal = Number($max.val());
            if( minVal === maxVal ){
                $min.css('z-index', minVal===10 ? 4 : 3)
                $max.css('z-index', minVal===0 ? 4 : 3)
            }
            else{
                $min.css('z-index', 4)
                $max.css('z-index', 4)
            }
            $params.find('#fill').css({left: minVal*10+'%', width: (maxVal-minVal)*10+'%'});
            $params.find('.label').each((i,el)=> {el.classList.toggle('active', i===minVal || i===maxVal)})
            this.current[index].value[0] = validValues[minVal];
            this.current[index].value[1] = validValues[maxVal];
        },
        filterEnergy: function (e){
            const index = this.current.findIndex(item => item.name === "energy");
            const validValues = ['<0.1cll', '0.5cll', '1cll', '5cll', '10cll', '20cll', '40cll', '80cll', '160cll', '320cll', '>500cll'];
            const $energy = $('#energyFilter');
            const $min = $energy.find('#min');
            const $max = $energy.find('#max');
            let minVal = Number($min.val());
            let maxVal = Number($max.val());
            if(e){
                if(e.target===$min[0] && minVal >= maxVal && maxVal !==10 ) $min.val(maxVal-1);
                else if( e.target === $max[0] && maxVal <= minVal && minVal !==0 ) $max.val(minVal+1);
            }
            minVal = Number($min.val());
            maxVal = Number($max.val());
            if( minVal === maxVal ){
                $min.css('z-index', minVal===10 ? 4 : 3)
                $max.css('z-index', minVal===0 ? 4 : 3)
            }
            else{
                $min.css('z-index', 4)
                $max.css('z-index', 4)
            }
            $energy.find('#fill').css({left: minVal*10+'%', width: (maxVal-minVal)*10+'%'});
            $energy.find('.label').each((i,el)=> {el.classList.toggle('active', i===minVal || i===maxVal)})
            this.current[index].value[0] = validValues[minVal];
            this.current[index].value[1] = validValues[maxVal];
        },
        filterInfo: function(e) {
            const index = this.current.findIndex(item => item.name === "info");
            this.current[index].value = $(e.currentTarget).val();
            $('.info-value').text(this.current[index].value);
            $(e.currentTarget).css('background', 'linear-gradient(90deg, var(--text-primary) '+ this.current[index].value + '%, var(--bg-tertiary) '+this.current[index].value+'%)');
        },
        filterTask: function(e) {
            const $target = $(e.target)
            if ($target.hasClass('filter-optgroup')) {
                // multiple selection
                $target.toggleClass("active");
                if ($target.hasClass('active')){
                    $target.nextUntil('.filter-optgroup', '.filter-option:not(.active)').trigger('click');
                }
                else{
                    $target.nextUntil('.filter-optgroup', '.filter-option.active').trigger('click');
                }
            }
            const option = $target.attr('data-filter')
            if (!(option && $target.hasClass('filter-option'))) return;
            $target.toggleClass("active");
            const index = this.current.findIndex(item => item.name === "task");
            if(this.current[index].value.includes(option)){
                this.current[index].value.splice(this.current[index].value.indexOf(option), 1);
            }
            else {
                this.current[index].value.push(option);
            }
            // check if optgroup must have active class
            const optgroup = $target.prevAll('.filter-optgroup').first();
            const options = optgroup.nextUntil('.filter-optgroup', '.filter-option');
            if (options.length > 0 && options.filter('.active').length === options.length) {
                optgroup.addClass('active');
            } else {
                optgroup.removeClass('active');
            }
        },
        filterType: function(e) {
            const $target = $(e.target)
            if ($target.hasClass('filter-optgroup')) {
                // multiple selection
                $target.toggleClass("active");
                if ($target.hasClass('active')){
                    $target.nextUntil('.filter-optgroup', '.filter-option:not(.active)').trigger('click');
                }
                else{
                    $target.nextUntil('.filter-optgroup', '.filter-option.active').trigger('click');
                }
            }
            const option = $target.attr('data-filter')
            if (!(option && $target.hasClass('filter-option'))) return;
            $target.toggleClass("active");
            const index = this.current.findIndex(item => item.name === "type");
            if(this.current[index].value.includes(option)){
                this.current[index].value.splice(this.current[index].value.indexOf(option), 1);
            }
            else {
                this.current[index].value.push(option);
            }
            // check if optgroup must have active class
            const optgroup = $target.prevAll('.filter-optgroup').first();
            const options = optgroup.nextUntil('.filter-optgroup', '.filter-option');
            if (options.length > 0 && options.filter('.active').length === options.length) {
                optgroup.addClass('active');
            } else {
                optgroup.removeClass('active');
            }
        },
        newFilter: function() {
            this.templates.modal.render();
        },
        removeFilter: function(event) {
            const $el = $(event.target).closest('p');
            const filter = $el.attr('data-filter');
            delete this.filters[filter];
            $el.next('br').remove();
            $el.remove();
            this.options[filter].active = false;
            this.request();
        },
        topicCallback: function () {
                const now = Date.now();
                if (now - this.lastUpdate < this.delay && !this.first) {
                    clearTimeout(this.pending);
                    this.pending = setTimeout(this.request.bind(this), this.delay);
                    return;
                }
                this.lastUpdate = now;
                this.filters.query = this.$topic.val().trim();
                this.request();
            },
        request: function() {
            if (this.first) $('#loading').show();
            $.ajax({
                url: "/transparency/cards",
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify(this.filters),
                success: r => {
                    $('#loading').hide();
                    const results = r.results || [];
                    
                    $('#search_results_wrapper').text("Showing");
                    $('#search_results').text(results.length + " of " + (r.total || 0));
                    this.$tbody.empty();

                    if (results.length)
                        results.forEach(it => {
                            const name = it.name.replace(new RegExp("(" + this.filters.query + ")", "ig"),"<strong style='color:#79CFDC'>$1</strong>");
                            const type = (it.type || it.task || "").toLowerCase();
                            const task = it.task ? " for " + it.task.toLowerCase() : "";
                            const params = it.parameters && it.parameters[0] !==0 ? it.parameters : null;
                            this.$tbody.append(this.templates.cardRow.render(it, name, type, task, params));
                        });
                    else this.$tbody.append(`<tr><td colspan="3" style="text-align:center;color: var(--text-primary);font-weight:bold;font-size:22px;">No matching results</td></tr>`);
                    $("#resultsTable").show();
                    if(r.total===results.length || results.length<50) $('#total-count').text(results.length + ' found model cards');
                    else $('#total-count').text("Top "+results.length+" found model cards (database size: "+r.total + ')');
                    this.first = false;
                },
                error: () => {
                    $('#loading').hide();
                    this.first = false;
                    console.error("Error fetching results");
                }
            });
        },
        dashboardRender: function(event){
            const selectedDashboard = $(event.target).val();
            $filterdashboard = $(".filter-dashboard");
            $filterdashboard.attr('data-filter', selectedDashboard);
            $dashboard = $(".dashboard");
            const index = this.current.findIndex(item => item.name === selectedDashboard);
            if (index === -1){
                this.appendToCurrent(selectedDashboard);
            }
            $filterdashboard.css('overflow-y', 'hidden');
            $dashboard.slideUp(300, function() {
                $filterdashboard.html(this.dashboards[selectedDashboard].html);
                $('.dashboard-description').text(this.dashboards[selectedDashboard].description);
                this.dashboards[selectedDashboard].setState();
                $dashboard.slideDown(400, function(){
                    $filterdashboard.css('overflow-y', 'auto');
                });
            }.bind(this));
        },
        modalRender: function (){
            this.$modal.addClass('modal--active').html(this.templates.modal.template);
            $dashboard = $(".dashboard");
            $dashboard.hide();
            $('.filter-title h1').text('Filters')
            Object.keys(this.options).forEach(filter => {
                if (this.options[filter].active) return;
                $('<option>')
                    .val(filter)
                    .text(capitalizeFirstLetter(filter))
                    .appendTo(this.$modal.find('#filter-select'));
            });
        },
        cardRowRender: function (it, name, type, task, params) {
            const percent = Math.round(it.quality * 100);
            const qualityColor =
                percent > 70 ? 'var(--green-primary)' :
                percent > 40  ? 'var(--yellow-primary)' :
                '#F87F76';
            const energy= Math.max(0, Math.min(200, parseFloat(it.energy) || 0));
            const energyColor =
                100-energy/2 > 70 ? 'var(--green-primary)' :
                100-energy/2 > 40 ? 'var(--yellow-primary)' :
                '#F87F76';
            const view = {
                id: it.id,
                name: name,
                percent: percent,
                dashOffset: 100 - percent,
                qualityColor: qualityColor,
                description: it.description || "",
                energy: energy,
                hasEnergy: energy!==0,
                energyDashOffset: (energy / 2),
                energyColor: energyColor,
                isDraft: !it.desc,
                creatorText:
                    (it.desc || "") +
                    (it.creator ? " uploaded by " + it.creator : ""),
                hasType: !!type,
                type: type,
                task: task,
                hasParams: Boolean(params),
                params: params
            };
            return Mustache.render(this.templates.cardRow.template, view);
        },
        filtersRender: function() {
            this.$filters.html("");
            $('<p>')
                .attr('id', 'new-filter')
                .addClass('filter button modal__trigger')
                .attr('data-modal', '#filters')
                .html('<div><i class="fa-solid fa-plus"></i>&nbsp;&nbsp;New filter</div>')
                .appendTo(this.$filters);
            
        },
        appendToCurrent: function(filter) {
            if (filter === 'type'){ this.current.push({name: 'type', value: []}) }
            else if (filter === 'task'){ this.current.push({name: 'task', value: []}) }
            else if (filter === 'info'){ this.current.push({name: 'info', value: '0'}) }
            else if (filter === 'params'){ this.current.push({name: 'params', value: ['<1B','>500B']}) }
            else if (filter === 'energy'){ this.current.push({name: 'energy', value: ['<0.1cll','>500cll']}) }
        },
        getTaskDashboard: function () {
            return $.getJSON('/transparency/options/overview/task').then(function (data) {
                    const $element = $('<div>');
                    data.forEach(taskOption => {
                        const $span = $('<span>');
                        if (taskOption.startsWith("#")) {
                            $span
                                .text(taskOption.replace("#", ""))
                                .addClass("filter-optgroup");
                        } else {
                            $span
                                .text(taskOption)
                                .addClass("filter-option")
                                .attr("data-filter", taskOption);
                        }
                        $element.append($span);
                    });
                    return $element.html();
                })
                .catch(function (err) {
                    console.error(err);
                });
        },
        getTypeDashboard: function() {
            return $.getJSON('/transparency/options/overview/type').then(function(data) {
                const $element = $('<div>');
                data.forEach(typeOption => {
                    const $span = $('<span>');
                    if (typeOption.startsWith("#")) {
                        $span
                            .text(typeOption.replace("#", ""))
                            .addClass("filter-optgroup");
                    } else {
                        $span
                            .text(typeOption)
                            .addClass("filter-option")
                            .attr("data-filter", typeOption);
                    }
                    $element.append($span);
                });
                return $element.html()
            }.bind(this))
            .fail((err) => {
                console.error(err);
            });
        }, 
        getInfoDashboard: function () {
            return '<div id="infoFilter">Info at least <span class="info-value">0</span>% <input type="range" class="info-input" min="0" max="100" step="1" value="0"/></div>'
        },
        getParamsDashboard: function() {
            return $.get('templates/index/paramsDashboard.mustache')
                .then(function(template) {
                    return Mustache.render(template, {});
                });
        },
        getEnergyDashboard: function() {
            return $.get('templates/index/energyDashboard.mustache')
                .then(function(template) {
                    return Mustache.render(template, {});
                });
        },
        done: function() {
            for (let current of this.current) {
                if (!(this.options[current.name].active)) {
                    if (
                        (current.name === 'info' && current.value === '0') ||
                        (current.name === 'params' && !current.value[0] || (current.value[0] === '<1B' && current.value[1] === '>500B')) || 
                        (current.name === 'energy' && !current.value[0] || (current.value[0] === '<0cll' && current.value[1] === '>500cll'))
                    ) {
                        this.$modal.removeClass('modal--active');
                        continue;
                    }
                    this.addfilter(current.name);
                    this.options[current.name].active = true;
                }
                this.filters[current.name] = current.value;
                this.captions[current.name].update()
                this.$modal.removeClass('modal--active');
                $('#edit-filter').each(function () {
                    const spans = $(this).find('span');
                    if (spans.length === 1) {
                        spans.trigger('click');
                    }
                });
            }
            this.current = []
            this.request();
        },
        cancel: function() {
            this.$modal.removeClass('modal--active');
        },
        addfilter: function(filter) {
            var newP = $('<p>');
            newP
                .attr('data-filter', filter)
                .attr('id', 'edit-filter')
                .addClass('filter button secondary success')
            this.$filters.children('p').eq(-1).before(newP);
            this.$filters.children('p').eq(-1).before(newP, $('<br>'));

        },

        loadTemplates: async function(templates) {
            const keys = Object.keys(templates);
            const promises = keys.map(key => $.get(templates[key].path));
            
            const results = await Promise.all(promises);
            
            results.forEach((template, index) => { 
                if (keys[index] === "editModal") {
                    const $html = $('<div>').html(template);
                    $html.find('label[for="filter-select"]').remove();
                    $html.find('select#filter-select').remove();
                    template = $html.html();
                }
                templates[keys[index]].template = template;
            });
        }
    };

    function capitalizeFirstLetter(val) {
        return String(val).charAt(0).toUpperCase() + String(val).slice(1);
    }
    function noLineBreak(string) {
        return string.replaceAll(' ', '&nbsp;').replaceAll('-', '&#8209;')
    }

    filters.init();
})