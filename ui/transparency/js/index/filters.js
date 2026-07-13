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
    var userFilterOn = false;
    var draftFilterOn = false;

    var filters = {
        filters: {}, // goes to backend
        templates: {}, // {name: {template: .mustache, render: function()},...}
        options: {}, // dropdown menu
        dashboards: {}, // html strings e.g. {type: "...",...}
        current:{}, // current editable filter {name:, value:}
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
            this.dashboards.task = {html: "", setState: this.taskSetState.bind(this), description: 'Filter Model Cards by task.'};
            this.dashboards.type = {html: "", setState: this.typeSetState.bind(this), description: 'Filter Model Cards by type.'};
            this.dashboards.info = {html: "", setState: this.infoSetState.bind(this), description: 'Show only model cards based on how complete their information is.'};
            this.getTaskDashboard().then(function (html) { this.dashboards.task.html = html; }.bind(this));
            this.getTypeDashboard().then(function (html) { this.dashboards.type.html = html; }.bind(this));
            this.dashboards.info.html = this.getInfoDashboard();
        },

        init_captions: function() {
            this.captions.task = {update: this.updateTaskCaption.bind(this)};
            this.captions.type = {update: this.updateTypeCaption.bind(this)};
            this.captions.info = {update: this.updateInfoCaption.bind(this)};
        },

        init_options: function() {
            this.options.task = {active: false};
            this.options.type = {active: false};
            this.options.info = {active: false};
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

        captionBuilder: function(filter, value){
            const icon = '<i class="fa-solid fa-pencil"></i>'
            const $caption = $('<div>').html(`${icon}&nbsp;${capitalizeFirstLetter(filter)}:  ${value}`);
            const $cancel = $('<div>').html(`<span class="remove-filter">X</span>`);
            this.$filters.find(`[data-filter="${filter}"]`).empty().append($caption).append($cancel);
        },

        taskSetState: function() {
            this.current.value.forEach(function(task){
                this.$modal.find('[data-filter="' + task + '"]').addClass("active");
            }.bind(this));
        },
        typeSetState: function() {
            this.current.value.forEach(function(type){
                this.$modal.find('[data-filter="' + type + '"]').addClass("active");
            }.bind(this));

        },
        infoSetState: function() {
            $('.info-input')
                .val(this.current.value)
                .css('background', 'linear-gradient(90deg, #3e3e3e '+ this.current.value + '%, #EEEEEE '+this.current.value+'%)');
            $('.info-value').text(this.current.value);
            
        },
        editFilter: function(e) {
            if ($(e.target).closest('.remove-filter').length) return;
            const filter = $(e.currentTarget).attr('data-filter');
            this.current = {name: filter, value: this.filters[filter]};
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

        filterInfo: function(e) {
            this.current.value = $(e.currentTarget).val();
            $('.info-value').text(this.current.value);
            $(e.currentTarget).css('background', 'linear-gradient(90deg, #3e3e3e '+ this.current.value + '%, #EEEEEE '+this.current.value+'%)');
        },
        filterTask: function(e) {
            const $target = $(e.target)
            const option = $target.attr('data-filter')
            if (!(option && $target.hasClass('filter-option'))) return;
            $target.toggleClass("active");
            if(this.current.value.includes(option)){
                this.current.value.splice(this.current.value.indexOf(option), 1);
            }
            else {
                this.current.value.push(option);
            }
        },
        filterType: function(e) {
            const $target = $(e.target)
            const option = $target.attr('data-filter')
            if (!(option && $target.hasClass('filter-option'))) return;
            $target.toggleClass("active");
            if(this.current.value.includes(option)){
                this.current.value.splice(this.current.value.indexOf(option), 1);
            }
            else {
                this.current.value.push(option);
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
                            this.$tbody.append(this.templates.cardRow.render(it, name, type, task));
                        });
                    else this.$tbody.append(`<tr><td colspan="3" style="text-align:center;color: var(--text-primary);font-weight:bold;font-size:22px;">No matching results</td></tr>`);
                    $("#resultsTable").show();
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
            this.setCurrent(selectedDashboard);
            $filterdashboard.css('overflow-y', 'hidden');
            $dashboard.slideUp(300, function() {
                $filterdashboard.html(this.dashboards[selectedDashboard].html);
                $('.dashboard-description').text(this.dashboards[selectedDashboard].description);
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
        cardRowRender: function (it, name, type, task) {
            const percent = Math.round(it.quality * 100);
            const qualityColor =
                it.quality > 0.7 ? 'var(--green-primary)' :
                it.quality > 0.4 ? 'var(--yellow-primary)' :
                '#F87F76';
            const view = {
                id: it.id,
                name: name,
                percent: percent,
                dashOffset: 100 - percent,
                qualityColor: qualityColor,
                description: it.description || "",
                isDraft: !it.desc,
                creatorText:
                    (it.desc || "") +
                    (it.creator ? " uploaded by " + it.creator : ""),
                hasType: !!type,
                type: type,
                task: task
            };
            return Mustache.render(this.templates.cardRow.template, view);
        },
        filtersRender: function() {
            this.$filters.html("");
            $('<p>')
                .attr('id', 'new-filter')
                .addClass('filter button modal__trigger')
                .attr('data-modal', '#filters')
                .html('<div><i class="fa-solid fa-plus"></i>&nbsp;&nbsp;New Filter</div>')
                .appendTo(this.$filters);
            
        },
        setCurrent: function(filter) {
            if (filter === 'type'){ this.current = {name: 'type', value: []} }
            else if (filter === 'task'){ this.current = {name: 'task', value: []} }
            else if (filter === 'info'){ this.current = {name: 'info', value: ''} }
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
            return 'Info at least <span class="info-value">0</span>% <input type="range" class="info-input" min="0" max="100" step="1" value="0"/>'
        },
        done: function() {
            if ((Array.isArray(this.current.value) && this.current.value.length === 0) || this.current.value === '' || !this.current.name) { 
                this.$modal.removeClass('modal--active');
                return 
            }
            if (!(this.options[this.current.name].active)) {
                this.addfilter(this.current.name);
                this.options[this.current.name].active = true;
            }
            this.filters[this.current.name] = this.current.value;
            this.captions[this.current.name].update()
            this.request();
            this.$modal.removeClass('modal--active');
            this.current = {};
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