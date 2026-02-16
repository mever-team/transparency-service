$(function () {
    var userFilterOn = false;
    var draftFilterOn = false;

    var filters = {
        filters: {}, // goes to backend
        templates: {}, // {name: {template: .mustache, render: function()},...}
        options: {}, // dropdown menu
        dashboards: {}, // html strings e.g. {type: "...",...}
        current:{}, // current editable filter
        lastUpdate: 0,
        pending: null,
        first: true,
        delay: 150,

        init: async function() {
            await this.init_templates();
            this.init_filters();
            this.init_options();
            await this.init_dashboards();
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
            this.getTaskDashboard().then(function (html) { this.dashboards.task = html; }.bind(this));
            this.getTypeDashboard().then(function (html) { this.dashboards.type = html; }.bind(this));
            this.dashboards.info = this.getInfoDashboard();
        },

        init_options: function() {
            this.options.task = {active: false};
            this.options.type = {active: false};
            this.options.info = {active: false};
        },

        init_templates: async function () {
            this.templates.cardRow = {template: "", render: this.cardRowRender.bind(this)};
            this.templates.modal = {template: "", render: this.modalRender.bind(this)};
            const [cardRowTemplate, modalTemplate] = await Promise.all([
                $.get("templates/index/cardRow.mustache"),
                $.get("templates/index/filtersModal.mustache")
            ]);
            this.templates.cardRow.template = cardRowTemplate;
            this.templates.modal.template = modalTemplate;
        },

        init_filters: function() {
            this.filters.drafts = false; 
            this.filters.user = false;
            this.filters.query = localStorage.getItem("last_search_term") || '';
        },

        bindEvents: function() { 
            this.$filters.on('click', '#new-filter', this.newFilter.bind(this));
            this.$filters.on('click', '.remove-filter', this.removeFilter.bind(this))
            this.$modal.on('change', '#filter-select', this.dashboardRender.bind(this))
            this.$topic.on("keyup", this.topicCallback.bind(this));
            this.$modal.on('click', '.filter-done', this.done.bind(this))
            this.$filters.on('click', '#user-filter', this.toggleUserFilter.bind(this));
            this.$filters.on('click', '#draft-filter', this.toggleDraftFilter.bind(this));
            this.$modal.on('click', '.filter-dashboard[data-filter="task"]', this.filterTask.bind(this))
            this.$modal.on('click', '.filter-dashboard[data-filter="type"]', this.filterType.bind(this))
            this.$modal.on('keyup', '.filter-dashboard[data-filter="info"] .info-input', this.filterInfo.bind(this))
        },


        ////////////////////////////
        //       Ugly Logic       //
        ////////////////////////////

        filterInfo: function(e) {
            this.current.value = Math.min(Math.max($(e.currentTarget).val(), 0), 100);
            $(e.currentTarget).val(this.current.value);
        },
        filterTask: function(e) {
            if (!e.target.id) return;
            $(e.target).toggleClass("active");
            if(this.current.value.includes(e.target.id)){
                this.current.value.splice(this.current.value.indexOf(e.target.id), 1);
            }
            else {
                this.current.value.push(e.target.id);
            }
        },
        filterType: function(e) {
            if (!e.target.id) return;
            $(e.target).toggleClass("active");
            if(this.current.value.includes(e.target.id))
                this.current.value.splice(this.current.value.indexOf(e.target.id), 1);
            else
                this.current.value.push(e.target.id);
        },
        newFilter: function() {
            this.templates.modal.render();
        },
        removeFilter: function(event) {
            const $el = $(event.target).closest('p');
            const filter = $el.attr('data-filter');
            delete this.filters[filter];
            $el.remove();
            this.options[filter].active = false;
            this.request();
        },
        toggleUserFilter: function () {
                const username = $('#account-name').text().trim();
                if (!username) return;
                userFilterOn = !userFilterOn;
                $('#user-filter').toggleClass('success', userFilterOn);
                const now = Date.now();
                if (now - this.lastUpdate < this.delay && !this.first) {
                    clearTimeout(this.pending);
                    this.pending = setTimeout(this.request.bind(this), this.delay);
                    return;
                }
                this.lastUpdate = now;
                this.filters.user = Boolean(this.filters.user ^ true);
                this.request();
            },
        toggleDraftFilter: function () {
                const username = $('#account-name').text().trim();
                if (!username) return;
                draftFilterOn = !draftFilterOn;
                $('#draft-filter').toggleClass('success', draftFilterOn);
                const now = Date.now();
                if (now - this.lastUpdate < this.delay && !this.first) {
                    clearTimeout(this.pending);
                    this.pending = setTimeout(this.request.bind(this), this.delay);
                    return;
                }
                this.lastUpdate = now;
                this.filters.drafts = Boolean(this.filters.drafts ^ true);
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
                    else this.$tbody.append(`<tr><td colspan="3" style="text-align:center;color:#EEEEEE;font-weight:bold;font-size:22px;">No matching results</td></tr>`);
                    $("#resultsTable").show();
                    localStorage.setItem("last_search_term", this.filters.query);
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
            $dashboard.slideUp(300, function() {
                $filterdashboard.html(this.dashboards[selectedDashboard]);
                $dashboard.slideDown();
            }.bind(this));
        },
        modalRender: function (){
            this.$modal.addClass('modal--active').html(this.templates.modal.template);
            $dashboard = $(".dashboard");
            $dashboard.hide();
            Object.keys(this.options).forEach(filter => {
                if (this.options[filter].active) return;
                $('<option>')
                    .val(filter)
                    .text(formatDisplayName(filter))
                    .appendTo(this.$modal.find('#filter-select'));
            });
        },
        cardRowRender: function (it, name, type, task) {
            const percent = Math.round(it.quality * 100);
            const qualityColor =
                it.quality > 0.7 ? '#6CC06B' :
                it.quality > 0.4 ? '#FBC483' :
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
                .attr('id', 'user-filter')
                .addClass('filter button secondary')
                .html('<div><i class="fa-solid fa-plus"></i>&nbsp;&nbsp;My cards only</div>')
                .css('display', token?'auto':'none')
                .appendTo(this.$filters);
            $('<p>')
                .attr('id', 'draft-filter')
                .addClass('filter button secondary')
                .html('<div><i class="fa-solid fa-plus"></i>&nbsp;&nbsp;Show drafts</div>')
                .appendTo(this.$filters);
            $('<p>')
                .attr('id', 'new-filter')
                .addClass('filter button secondary modal__trigger')
                .attr('data-modal', '#filters')
                .html('<div><i class="fa-solid fa-plus"></i>&nbsp;&nbsp;Add filter</div>')
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
                                .attr("id", taskOption);
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
                            .attr("id", typeOption);
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
            return '<br>Minimum completion<br><input type="number" class="info-input"/>&nbsp;%'
        },
        done: function() {
            if ((Array.isArray(this.current.value) && this.current.value.length === 0) || this.current.value === '' || !this.current.name) { 
                this.$modal.removeClass('modal--active');
                return 
            }
            this.filters[this.current.name] = this.current.value;
            this.options[this.current.name].active = true;
            this.request();
            this.addfilter(this.current.name);
            this.$modal.removeClass('modal--active');
        },
        addfilter: function(filter) {
            var newP = $('<p>');
            newP
                .attr('data-filter', filter)
                .addClass('filter button secondary success')
                .html('<div>✏️&nbsp;'+formatDisplayName(filter)+'</div><span class="remove-filter">X</span>')
            this.$filters.children('p').eq(-1).before(newP);
        }
    };

    function formatDisplayName(val) {return "Model "+val;}

    filters.init();
})