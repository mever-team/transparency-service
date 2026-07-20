$(function() {
    let cardJson;
    let comparedJson;
    let comparedJsonSimple;
    let menuOffsetTop=0;
    let editor;
    let turndownService = null;
    let markedInstance = null;

    // Custom MediumEditor extension for inserting code blocks
    function getHighestPreFromNode(node) {
        let current = node;
        let highestPre = null;

        while (current) {
            if (current.nodeType === 1 && current.tagName === "PRE") {
            highestPre = current;
            }
            current = current.parentNode;
        }

        return highestPre;
    }
    function getHighestPreFromCursor() {
        const selection = window.getSelection();
        if (!selection.rangeCount) return null;
        let node = selection.anchorNode;
        if (node.nodeType === 3) {
            node = node.parentElement;
        }
        return getHighestPreFromNode(node);
    }
    var CodeBlockButton = MediumEditor.Extension.extend({
        name: 'codeblock',

        init: function () {
            this.button = document.createElement('button');
            this.button.classList.add('medium-editor-action');
            this.button.innerHTML = '&lt;/&gt;';
            this.button.title = 'Code Block';
            this.button.onclick = this.handleClick.bind(this);
        },

        getButton: function () {
            return this.button;
        },

        handleClick: function (event) {
            this.action();
        },

        checkState: function (node) {
            var sel = window.getSelection();
            if (!sel.rangeCount) {
                this.button.classList.remove('medium-editor-button-active');
                return false;
            }

            var range = sel.getRangeAt(0);
            var container = range.commonAncestorContainer;
            var el = container.nodeType === 3 ? container.parentElement : container;
            var inside = !!el.closest('pre');

            this.button.classList.toggle('medium-editor-button-active', inside);

            // disable other buttons
            var toolbar = this.base.getExtensionByName('toolbar');
            if (toolbar && toolbar.getToolbarElement) {
                var buttons = toolbar.getToolbarElement().querySelectorAll('button');

                buttons.forEach((btn) => {
                    if (btn === this.button) {
                        btn.disabled = false;
                    } else {
                        btn.disabled = inside;
                    }
                    // console.log(btn);
                });
            }
            return inside;
        },

        // Toggle behavior
        action: function () {
            var editor = this.base;
            var selection = window.getSelection();
            if (!selection || selection.rangeCount === 0) return;

            var range = selection.getRangeAt(0);
            var container = range.commonAncestorContainer;
            var el = container.nodeType === 3 ? container.parentElement : container;
            var preElement = el.closest('pre');

            if (preElement) {
                const parentPre = getHighestPreFromCursor();
                const range = document.createRange();
                range.selectNodeContents(parentPre);
                const selection = window.getSelection();
                selection.removeAllRanges();
                selection.addRange(range);
                document.execCommand('formatBlock', false, 'div');
                
            } else {
                document.execCommand('formatBlock', false, 'pre');
                // preElement = window.getSelection().focusNode.parentNode;
                if (selection.rangeCount > 0) {
                    let node = selection.getRangeAt(0).startContainer;
                    if (node.nodeType === Node.TEXT_NODE) {
                        node = node.parentElement;
                    }
                    preElement = node.closest('pre');
                }
                preElement.innerHTML = preElement.innerHTML.replaceAll("<br>", "\n");
                hljs.highlightElement(preElement);
                preElement.setAttribute('spellcheck', 'false');
                preElement.setAttribute('autocorrect', 'off');
                preElement.setAttribute('autocapitalize', 'off');
                preElement.setAttribute('translate', 'no');
            }

            // Notify the editor that content changed
            var editable = editor.elements[0];
            if (editable) {
                $(editable).trigger('input');
                $(editable).trigger('editableInput');
            }
            this.checkState();
        }
    });

    function initConverters() {
        function getPreText(node) {
            let text = '';
            for (const child of node.childNodes) {
                if (child.nodeType === Node.TEXT_NODE) {
                    text += child.textContent;
                } else if (child.nodeType === Node.ELEMENT_NODE) {
                    if (child.tagName === 'BR') {
                        text += '\n';
                    } else {
                        text += getPreText(child);
                    }
                }
            }
            return text;
        }

        // ---------- Turndown ----------
        if (typeof TurndownService !== 'undefined' && !turndownService) {
            turndownService = new TurndownService({
                headingStyle: 'atx',
                codeBlockStyle: 'fenced'
            });
            turndownService.keep(['sub', 'sup', 'u', 'ins']);

            // Custom rule for <pre>
            turndownService.addRule('pre', {
                filter: 'pre',
                replacement: function(content, node) {
                    const codeText = getPreText(node);
                    return '```\n' + codeText + '\n```';
                }
            });
        }

        // ---------- Marked ----------
        if (typeof marked !== 'undefined' && !markedInstance) {
            markedInstance = marked;
            markedInstance.setOptions({ breaks: true, gfm: true });

            // Renderer to output plain <pre>
            const renderer = {
                code(token) {
                    const codeText = (token.text || token);
                    const language = token.lang || '';
                    const langAttr = language ? ` class="language-${language}"` : '';
                    return `<pre${langAttr}>${codeText}</pre>`;
                }
            };
            markedInstance.use({ renderer });
        }
    }

    function htmlToMarkdown(html) {
        initConverters();

        if (!turndownService) return html;
        if (!html || typeof html !== 'string') return '';

        const container = document.createElement('div');
        container.innerHTML = html;

        return turndownService.turndown(container.innerHTML);
    }

    function markdownToHtml(md) {
        initConverters();
        if (!markedInstance) return md;
        if (!md || typeof md !== 'string') return '';
        return markedInstance.parse(md);
    }

    function error_message(message) {
        console.log(message);
        $('#popup-error-screen').css('display' , 'flex');
        if(message) $('#error-message').html(message);
    }

    function error_handler(xhr, status, error) {
        try {
            const resp = JSON.parse(xhr.responseText);
            error_message(resp.error || error);
        }
        catch(e) { error_message(""); }
    }

    // Close confirmation modal
    $('#cancel-delete-btn').on('click', function () {$('#delete-confirm-screen').css('display' , 'none')});
    $('#cancel-report-btn').on('click', function () {$('#report-confirm-screen').css('display' , 'none')});
    $('#cancel-autocomplete-btn').on('click', function () {$('#modal-autocomplete-screen').css('display' , 'none')});
    $('#cancel-refine-btn').on('click', function () {$('#modal-refine-screen').css('display' , 'none')});

    $(document).on("click", ".naccs .menu div", function () {
        let numberIndex = $(this).index();
        if (!$(this).is("active")) {
            $(".naccs .menu div").removeClass("active");
            $(".naccs ul li").removeClass("active");
            $(".naccs ul").children("li").eq(numberIndex).addClass("active");
            $(this).addClass("active");
        }
    });


    $(document).on('keydown', (e) => {
    if (e.key === 'Escape') {
        const modals = [
            'delete-confirm-screen',
            'report-confirm-screen', // TODO: iterate through all these modals vias their common class selector instead
            'modal-autocomplete-screen',
            'modal-refine-screen',
            'popup-error-screen',
            'delete-success-screen',
            'card-locked',
            'modal-autocomplete-screen',
        ];
        modals.forEach(id => {
            const $el = $(`#${id}`);
            if ($el.length && $el.is(':visible')) $el.hide();
        });
    }
    });

    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    const compareto = urlParams.get('compareto');
    const $menu = $('.menu');
    // $menu.css({visibility: 'hidden', display: 'block'});
    // let menuOffsetTop = $menu.offset().top; // this will be updated, depending on history taking up space
    // $menu.css({visibility: '',display: 'none'});
    const pageUrl = encodeURIComponent(window.location.href);
    const pageTitle = encodeURIComponent(document.title);
    $('#pdf_desc').hide();
    $('#metrics_desc').hide();
    $("#share-banner").attr("href", `/transparency/banner/${id}`);
    $("#share-x").attr("href", `https://twitter.com/intent/tweet?url=${pageUrl}&text=${pageTitle}`);
    $("#share-facebook").attr("href", `https://www.facebook.com/sharer/sharer.php?u=${pageUrl}`);
    $("#share-linkedin").attr("href", `https://www.linkedin.com/shareArticle?mini=true&url=${pageUrl}&title=${pageTitle}`);
    $("#share-whatsapp").attr("href", `https://wa.me/?text=${pageUrl}`);
    $("#share-telegram").attr("href", `https://t.me/share/url?url=${pageUrl}&text=${pageTitle}`);
    $('#account-btn').click(() => { window.location.href = 'account.html'; });

    $('#pdf_text').click(function () {
        $('.card-button#agent').attr('data-type', 'pdf');

        $('#url_text').removeClass('active');
        $('#card-url,#card-url-p').slideUp();
        $('#url_desc').slideUp();

        $('#pdf_text').addClass('active');
        $('#pdf-container').slideDown();
        $('#pdf_desc').slideDown();

        $('#metrics_text').removeClass('active');
        $('#metrics-container').slideUp();
        $('#metrics_desc').slideUp();
    });
    $('#url_text').click(function () {
        $('.card-button#agent').attr('data-type', 'url');

        $('#url_text').addClass('active');
        $('#card-url,#card-url-p').slideDown();
        $('#url_desc').slideDown();

        $('#pdf_text').removeClass('active');
        $('#pdf-container').slideUp();
        $('#pdf_desc').slideUp();

        $('#metrics_text').removeClass('active');
        $('#metrics-container').slideUp();
        $('#metrics_desc').slideUp();
    });
    $('#metrics_text').click(function () {
        $('.card-button#agent').attr('data-type', 'metrics');

        $('#url_text').removeClass('active');
        $('#card-url,#card-url-p').slideUp();
        $('#url_desc').slideUp();
        
        $('#pdf_text').removeClass('active');
        $('#pdf-container').slideUp();
        $('#pdf_desc').slideUp();

        $('#metrics_text').addClass('active');
        $('#metrics-container').slideDown();
        $('#metrics_desc').slideDown();
    });

    $('#simple-view').click(function(){
        $('#technical-view').removeClass('active');
        $('#simple-view').addClass('active');
        $menu.removeClass('active');
        $('.contents').addClass('simple');
        $('.nacc li').removeClass('active');
        $('.nacc li#simpleSection').addClass('active');
    })

    
    $('#technical-view').click(function(){
        $('#technical-view').addClass('active');
        $('#simple-view').removeClass('active');
        $menu.addClass('active');
        // $('.contents').css('margin-left', '190px')
        $('.contents').removeClass('simple');
        $('.nacc li').removeClass('active');
        $('.nacc li').first().addClass('active');
        $('.menu').find('div').removeClass('active');
        $('.menu div:first-child').addClass('active');
    })


    // $(window).on('scroll', function () {
    //     if ($(window).scrollTop() > menuOffsetTop - 20) $menu.addClass('fixed');
    //     else $menu.removeClass('fixed');
    // });
    // let interval = setInterval(function () {checkLocked(interval);}, 100); // do first run immediately
    let interval = null;
    function runRefinement(assistant, id) {
        $.ajax({
            url: "/transparency/assistant/" + assistant + '/refine/' + id,
            method: "POST",
            contentType: "application/json",
            dataType: "json",
            headers: {"Authorization": "Bearer " + token},
            success: function (response) {},
            error: error_handler
        });
    }
    function renderSection(section, index, comparedJson, is_logged_in, no_title=false){
        let baseSection = comparedJson&&comparedJson.data?comparedJson.data[index]:undefined;
        let sectionTitle = section.name.replace(/_/g, " ").toUpperCase();
        let $section = $("<section>");
        if (!no_title) $section.append($("<h2>").text(sectionTitle));
        if (!section.value.length) $section.append($("<p>").text("No data provided."));
        section.value.forEach((field, fieldIndex) => {
            let $field = $("<div>").addClass("field").attr('data-name', field.name.replace(/_/g, " "));

            // field-name
            let $fieldName = $("<span>")
                .addClass("field-name")
                .text(" "+field.name.replace(/_/g, " "));
            


            // info-tooltip
            let $fieldInfo = $("<span>")
                .addClass("info-tooltip")
                .attr("data-tooltip", field.description)
                .text("?");
            $fieldInfo = $("<span>").addClass("field-info").append($fieldInfo).append($fieldName);
            let $fieldValue;
            
        if (field.type.startsWith("list:") && is_logged_in) {
            // Parse the raw list
            const rawOptions = field.type.replace("list:", "").split(",");
            const groups = []; // { label: "GroupName", options: [...] }
            let currentGroup = null;
            
            rawOptions.forEach(opt => {
                if (opt.startsWith("#")) {
                    currentGroup = { label: opt.replace("#", ""), options: [] };
                    groups.push(currentGroup);
                } else if (currentGroup) {
                    currentGroup.options.push(opt);
                } else {
                    if (!groups[0]) groups.push({ label: "Options", options: [] });
                    groups[0].options.push(opt);
                }
            });

            // Flatten for search but keep group context for rendering
            const allOptions = groups.flatMap(g => g.options);
            
            // Create wrapper and input
            const $wrapper = $("<div>").addClass("autocomplete-wrapper");
            const $input = $("<input>").addClass("autocomplete-input editable").attr({
                type: "text",
                value: field.value || "",
                placeholder: "Type or select from list"
            });
            const $suggestions = $("<div>").addClass("autocomplete-suggestions").hide();
            
            $wrapper.append($input, $suggestions);
            $fieldValue = $wrapper;

            // Update suggestions with groups
            function updateSuggestions(filterText) {
                const filter = filterText.toLowerCase().trim();
                $suggestions.empty();
                
                let hasMatches = false;
                
                groups.forEach(group => {
                    const matchedOptions = group.options.filter(opt => 
                        filter === "" || opt.toLowerCase().includes(filter)
                    );
                    if (matchedOptions.length === 0) return;
                    hasMatches = true;
                    
                    const $groupHeader = $("<div>")
                        .addClass("autocomplete-group-header")
                        .text(group.label);
                    $suggestions.append($groupHeader);
                    
                    matchedOptions.forEach(opt => {
                        let displayHtml = opt;
                        const filterLower = filterText.toLowerCase().trim();
                        if (filterLower !== "") {
                            const index = opt.toLowerCase().indexOf(filterLower);
                            if (index !== -1) {
                                const before = opt.slice(0, index);
                                const match = opt.slice(index, index + filterLower.length);
                                const after = opt.slice(index + filterLower.length);
                                displayHtml = before + "<strong>" + match + "</strong>" + after;
                            }
                        }
                        const $sug = $("<div>")
                            .addClass("autocomplete-suggestion")
                            .html(displayHtml)
                            .attr("data-value", opt);
                        $sug.on("click", function() {
                            $input.val(opt);
                            field.value = opt;
                            $suggestions.hide();
                            $("#saveJson").fadeIn();
                        });
                        $suggestions.append($sug);
                    });
                });
                
                if (!hasMatches) {
                    $suggestions.hide();
                } else {
                    $suggestions.show();
                }
            }

            // Show suggestions on focus/input
            $input.on("focus", function() { updateSuggestions($input.val()); });
            $input.on("input", function() {
                updateSuggestions($input.val());
                field.value = $input.val();
                $("#saveJson").fadeIn();
            });

            // Hide suggestions when clicking outside
            $(document).on("click", function(e) {
                if (!$wrapper.is(e.target) && !$wrapper.has(e.target).length) {
                    $suggestions.hide();
                }
            });

        } else if (field.type === 'date') {
                $fieldValue = $("<input>", {type: "date", readonly: is_logged_in? false: true}).addClass("field-value").val(field.value || "");
                $fieldValue.on("change", function () {field.value = $(this).val();});
                if(is_logged_in) $fieldValue.attr("contenteditable", "true");
                
            } else {
                let displayHtml = field.value || "";
                if (!field.type.startsWith("list:") && field.type !== 'date') {
                    displayHtml = markdownToHtml(displayHtml);
                }
                $fieldValue = $("<span>").addClass("field-value").html(displayHtml);
                if(is_logged_in) $fieldValue.attr("contenteditable", "true");
            }

            if(is_logged_in) $fieldValue.addClass("editable");

            // Editable field value
            let val = String(field.value || "").trim();
            if ((val  !== "") && (val  !== "<br>") && (val  !== "unknown")) {
                $('.menu').find('div').eq(index).find('.light').removeClass('square');
                $('.menu').find('div').eq(index).find('.light').addClass('arrow');
            }

            let $refineBtn = $("<button>")
                .addClass("refine-field")
                .text("refine field");
            $field.append($fieldInfo).append($fieldValue);
            // if (token && cardJson.creator===loggedUser){
            //     $field.append($refineBtn);
            // }
            $section.append($field);

            // compared value
            if(baseSection && (baseSection.value[fieldIndex].value)!==(section.value[fieldIndex].value)) {
                //console.log(baseSection.value[fieldIndex]);
                let $baseFieldValue = $("<span>")
                        .addClass("field-value")
                        .html(baseSection.value[fieldIndex].value || "");
                let $fieldBase = $("<span>")
                    .addClass("field-name")
                    .addClass("comparison")
                    .text("difference");

                $field.append($fieldBase);
                $field.append($baseFieldValue);
            }
        });
        return $section;
    }
    function normalRender(interval=null){
        $('body').removeClass('no-overflow');
        $('#card-locked').css('display' , 'none');
        if (interval) clearInterval(interval);

        function _render() {
            if(!cardJson || !comparedJson) return;
            if (token && cardJson.creator===loggedUser){
                $('#technical-view').html('<span>Show full version and edit</span>')
            }
            let is_logged_in = token&&cardJson.creator === loggedUser;
            if(is_logged_in) {
                $('#reportCard').hide();
                $('#deleteCard').show();
                $('#import-btn').show();
            }

            let jsonData = cardJson;
            $("#model-title").text(jsonData.title);
            $("#model-description").html(jsonData.description+" uploaded by "+jsonData.creator);
            $("#model-pending").html(jsonData.description?"":"DRAFT (needs version to be searchable)");
            $("#model-quality").html(`
                    <svg class="quality-circle" viewBox="0 0 36 36">
                    <circle cx="18" cy="18" r="18" fill="none" stroke="var(--bg-tertiary)" stroke-width="3"/>
                    <circle cx="18" cy="18" r="18" fill="none" stroke="${jsonData.quality>0.7?'var(--green-primary)':jsonData.quality>0.4?'var(--yellow-primary)':'#F87F76'}" stroke-width="3"
                    stroke-dasharray="100" stroke-dashoffset="${100 - Math.round(jsonData.quality * 100)}"/>
                    <text x="18" y="14" class="quality-text"> ${Math.round(jsonData.quality * 100)}%</text>
                    <text x="18" y="24" class="quality-text">info</text>
                </svg>
            `);

            const $historyContainer = $("#history-dropdown");
            $historyContainer.html(""); // clear previous content
            if (jsonData.history) {
                renderHistoryGraph(
                    jsonData.history,
                    Number(id),
                    $historyContainer[0]
                );

            }


            // fill in fields
            const $ul = $(".nacc");
            $ul.empty();
            $('#loading').hide();
            jsonData.data.forEach((section, index) => {
                let $li = $("<li>");
                $section = renderSection(section, index, comparedJson, is_logged_in);
                $li.append($("<div>").append($section));
                $ul.append($li);
                $('.menu').find('div').removeClass('active');
                $('.menu div:first-child').addClass('active');

            });

            if (!($('.light.arrow').length > 0)&& is_logged_in) {
                // TODO: we have the option of just opening the import, which may be more practical
                $('#modal-autocomplete-screen').css('display' , 'flex');
            }
            // render syntax highlighting and remove autocorrect
            document.querySelectorAll('pre').forEach((block) => {hljs.highlightElement(block);});
            document.querySelectorAll('pre').forEach(el => {
                el.setAttribute('spellcheck', 'false');
                el.setAttribute('autocorrect', 'off');
                el.setAttribute('autocapitalize', 'off');
                el.setAttribute('translate', 'no');
            });


        }




        if(compareto) {
            $.ajax({
                url: "/transparency/card/" + compareto,
                method: "GET",
                contentType: "application/json",
                dataType: "json",
                success: function (jsonData) {
                    comparedJson = jsonData;
                    $.ajax({
                        url: "/transparency/card/simple/" + compareto,
                        method: "GET",
                        contentType: "application/json",
                        dataType: "json",
                        success: function (jsonData) {
                            comparedJsonSimple = jsonData;
                            _render();
                        },
                        error: function (xhr, status, error) {}
                    });
                    _render();
                },
                error: function (xhr, status, error) {}
            });
        }
        else{
            comparedJson = {}; // we use the existence of comparedJson as a mark for render()
            comparedJsonSimple = {};
        }

        $.ajax({
            url: "/transparency/card/" + id,
            method: "GET",
            contentType: "application/json",
            dataType: "json",
            success: function (jsonData) {
                cardJson = jsonData;

                _render();
                _renderSimple();
                if (token && cardJson.creator===loggedUser) {
                    render_emissions_flash();
                }
                editor = new MediumEditor('span.editable', {
                    placeholder: false,

                    toolbar: {
                        buttons: [
                            'bold',
                            'italic',
                            'underline',
                            'anchor',
                            // 'h2',
                            // 'h3',
                            'quote',
                            'orderedlist',
                            'unorderedlist',
                            'codeblock'
                        ],
                        static: true,
                        updateOnEmptySelection: true
                    }, 
                    extensions: {
                        codeblock: new CodeBlockButton()
                    }
                });

                editor.subscribe('showToolbar', function() {
                    var $toolbar = $('.medium-editor-toolbar');
                    if ($toolbar.length && !$toolbar.find('.undo-hint').length) {
                        $('<div class="undo-hint">⌨️ Ctrl+Z to undo</div>')
                            .prependTo($toolbar);
                    }
                });

                editor.subscribe('hideToolbar', function() {
                    $('.medium-editor-toolbar .undo-hint').remove();
                });
            },
            error: error_handler
        });

        
    }
    normalRender();
    function _renderWhileRefine(){
        const completed = {};
        let doneMenus = [];
        let firstpass = true;
        function isEmpty(obj) {
            for (const prop in obj) {
                if (Object.hasOwn(obj, prop)) {
                return false;
                }
            }
            return true;
        }
        let refineStarted = false;
        async function refineStatus(params) {
            $.ajax({
                url: "/transparency/job/" + id,
                method: "GET",
                headers: {"Authorization": "Bearer " + token},
                contentType: "application/json",
                dataType: "json",
                success: function (job) {
                    if (isEmpty(job)) {
                        clearInterval(intervalId);
                        if (refineStarted){
                            _renderSimple(true);
                            window.location.reload();
                        }
                        return;
                    }
                    if (job.operation !== "refine") {
                        clearInterval(intervalId);
                        if (refineStarted){
                            _renderSimple(true);
                            window.location.reload();
                        }
                        return;
                    }
                    if (!refineStarted){
                        $('#technical-view').trigger('click');
                        refineStarted = true;
                    }
                    // put loading spinners in UI
                    if (firstpass){
                        firstpass = false;
                        const $loading_field = $("<div>").addClass('fieldLoader');
                        const $loading_section = $("<span>").addClass('sectionLoader');
                        $('span.field-value').html($loading_field).attr('contenteditable', 'false');
                        $('.autocomplete-wrapper').each(function () {
                            const $input = $(this).find('.autocomplete-input');
                            const value = $input.val() || '';
                            $(this).replaceWith(`<span class="field-value">${value}</span>`);
                        });
                        $('input.field-value').each(function () {
                            const value = $(this).val() || '';
                            $(this).replaceWith(`<span class="field-value">${value}</span>`);
                        });
                        $('select.field-value').each(function () {
                            const value = $(this).val(); // or .find('option:selected').text() if you want text
                            $(this).replaceWith(`<span class="field-value">${value}</span>`);
                        });
                        //console.log($('.menu .light'));
                        $('.menu .light').hide();
                        $('.menu div').prepend($loading_section);
                    }
                    // poll update
                    for (const [section, fields] of Object.entries(job.data)) {
                        if (!completed[section]) {completed[section] = [];}
                        for (let [field, value] of Object.entries(fields)) {
                            field = field.replaceAll('_', ' ');
                            if (completed[section].includes(field)) {continue;}
                            let matched = false;
                            $('.contents .nacc li').each(function () {
                                const this_section = $(this).find('h2').first().text().trim().toLowerCase();
                                if (this_section === section) {
                                    $(this).find('.field').each(function () {
                                        const this_field = $(this).find('.field-name').text().trim().toLowerCase();
                                        if (this_field === field) {
                                        $(this)
                                            .find('span.field-value')
                                            .html(value)
                                            .fadeOut(0, function () {
                                                $(this)
                                                    // .attr('contenteditable', 'true')
                                                    .fadeIn(300);
                                            });
                                            matched = true;
                                            completed[section].push(field);
                                            return false; // break .each()
                                        }
                                    });
                                    return false; // break outer .each()
                                }
                            });
                            // update menu
                            $('.contents .nacc li').each(function () {
                                const this_section = $(this).find('h2').first().text().trim().toLowerCase();
                                if (($(this).find('.fieldLoader').length === 0) && !doneMenus.includes(this_section)) {
                                    $('.menu div').each(function (){
                                        if ($(this).html().toLowerCase().includes(this_section)) {
                                            doneMenus.push(this_section);
                                            $(this).find('.light').css('display', 'inline-block');
                                            $(this).find('.sectionLoader').remove();
                                        }
                                    });
                                }
                            });
                            
                            if (matched) {
                                continue;
                            }
                        }
                    }
                },
                error: function (xhr, status, error) {
                    clearInterval(intervalId);
                    normalRender();
                    error_handler(xhr, status, error);
                }
            });
        }
        let intervalId = NaN;
        refineStatus();
        intervalId = setInterval(refineStatus, 2000); // INCREASED THIS INTERVAL BECAUSE IT WAS TOO INTENSIVE
    }
    function _renderSimple(fromRefine=false){
        $.ajax({
            url: "/transparency/card/simple/" + id,
            method: "GET",
            contentType: "application/json",
            dataType: "json",
            success: function (jsonData) {
                let is_logged_in = token&&cardJson.creator === loggedUser;
                // fill in fields
                const $ul = $(".nacc");
                isActive = $ul.find("li#simpleSection").hasClass("active");
                $ul.find("li#simpleSection").remove();
                jsonData.data.forEach((section, index) => {
                    let $li = $("<li>").attr('id', 'simpleSection');
                    $section = renderSection(section, index, comparedJsonSimple, false, true);
                    $li.append($("<div>").append($section));
                    $ul.append($li);
                    if (isActive){
                        $('#simple-view').trigger('click');
                    }
                    // $('.menu').find('div').removeClass('active');
                    // $('.menu div:first-child').addClass('active');
                });
                if (!fromRefine){
                    $('#simple-view').trigger('click');
                }
                if (token && !fromRefine){
                    _renderWhileRefine();
                }
            },
            error: error_handler
        });
    }
    function checkLocked(interval) {
        $.ajax({
            url: "/transparency/card/" + id + "/locked",
            method: "GET",
            contentType: "application/json",
            dataType: "json",
            success: function (jsonData) {
                if (jsonData !== "") {
                    $('#card-locked').css('display','flex');
                    $('#lock-msg-text').html(jsonData);
                    $('body').addClass('no-overflow');
                    $('#loading').hide();
                } else {
                    normalRender(interval);
                }
            },
            error: function (xhr, status, error) {
                try {
                    const resp = JSON.parse(xhr.responseText);
                    if (interval) clearInterval(interval);
                    $('#model-title').remove();
                    $('#loading').hide();
                    $('#loading').hide();
                    $('#share-options').hide();
                    $('#edit-options').hide();
                    $('#deleteCard').hide();
                    $('#reportCard').show();
                    $('.example_button').css('pointer-events', 'none');
                    if(resp.error || error) error_handler(xhr, status, error);
                } catch (e) { error_message(""); }
            }
        });
    }

    if(token)
        $.ajax({
            url: "/transparency/assistants",
            method: "GET",
            headers: {"Authorization": "Bearer " + token},
            success: function (response) {
                $(".assistants_wrapper").each(function () {
                    const $container = $(this);
                    $.each(response, function (index, item) {
                        const $tempDiv = $("<div>").html(item.desc);
                        const title = $tempDiv.find("h1").prop("outerHTML") || "";
                        $tempDiv.find("h1").remove();
                        const description = $.trim($tempDiv.text());
                        const $card = $("<button>", {
                            id: item.name,
                            class: "card-button button",
                            attr: {"data-type": "url"},
                            html: `<div class="desc">${title}</div>`//+`<div class="tooltip">${description}</div>`
                        });
                        $container.append($card);
                    });
                });
            },
            error: error_handler
        });

    $(".nacc").on("input", ".editable", function () {

        const $this = $(this);
        
        if ($this.hasClass("autocomplete-input")) return;
        
        const fieldName = $this.siblings(".field-info").text().replace("?", "").trim().toLowerCase().replace(/ /g, "_");
        const sectionName = $this.closest("section").find("h2").first().contents().filter((_, el) => el.nodeType === 3).text().toLowerCase().replace(/ /g, "_");

        let section = cardJson.data.find(s => s.name === sectionName);
        if (section) {
            let field = section.value.find(f => f.name === fieldName);
            $("#saveJson").fadeIn();
            if (field) {
                if(field.type.startsWith("list:")) {
                    // this has its own listener
                    return;
                } else if(field.type === 'date') {
                    field.value = $(this).val();
                } else {
                    field.value = htmlToMarkdown($(this).html());
                }
            }
        }
    });

    if(token) $("#edit-options").show();

$('.contents').on('click', '.refine-field', async function () {
    const container = $(this).parent();

    const section_name = $('.menu').find('.active span:eq(1)').text().trim().toLowerCase();
    const field_name = container.find('.field-info .field-name').text().trim().toLowerCase();
    const field_value_el = container.find('.field-value');

    const field_value = field_value_el.text().trim().toLowerCase();
    const assistant = 'agent';

    const response = await fetch(
        "/transparency/assistant/" + assistant + '/refinefield/' + id,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({ value: field_value })
        }
    );

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let buffer = "";
    let fullText = field_value_el.html() + "<br><br>";

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split("\n");
        buffer = lines.pop();

        for (const line of lines) {
            if (!line.trim()) continue;

            try {
                const json = JSON.parse(line);
                const content = json.message.content

                if (content) {
                    fullText += content;
                    field_value_el.html(fullText);
                }
            } catch (e) {
                console.error("Parse error:", line);
            }
        }
    }
});

    $("#saveJson").click(function () {
        $("#saveJson").fadeOut();
        $('.editable').each(function () {
            const $fieldValue = $(this);
            const fieldName = $fieldValue.siblings(".field-info").contents()[1]?.outerText.replace(":", "").trim().toLowerCase().replace(/ /g, "_");
            const sectionName = $fieldValue.closest("section").find("h2").contents().filter((_, el) => el.nodeType === 3).text().toLowerCase().replace(/ /g, "_");
            if (!fieldName || !sectionName) return;

            let section = cardJson.data.find(s => s.name === sectionName);
            if (section) {
                let field = section.value.find(f => f.name === fieldName);
                if (field && !field.type.startsWith("list:") && field.type !== 'date') {
                    // console.log(field.value);
                    field.value = htmlToMarkdown($fieldValue.html());
                    // console.log(field.value);
                }
            }
        });
        $.ajax({
            url: "/transparency/card/" + id,
            method: "PUT",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify(cardJson.data.filter(section => section.name !== "history")),
            headers: {"Authorization": "Bearer " + token},
            success: function (response) {
                $('.menu').find('div').find('.light').removeClass('arrow');
                $('.menu').find('div').find('.light').addClass('square');

                ["overview", "use", "training", "evaluation", "performance", "safety"].forEach((sectionName, index) => {
                    let section = cardJson.data.filter(section => section.name !== "history").find(s => s.name === sectionName);
                    let hasValue = false;

                    if (section && section.value) {
                        for (let field of section.value) {
                            if ((field.value.trim() !== "") && (field.value.trim() !== "<br>") && (field.value.trim() !== "unknown")) {
                                hasValue = true;
                                $('.menu').find('div').eq(index).find('.light').removeClass('square');
                                $('.menu').find('div').eq(index).find('.light').addClass('arrow');
                                break; // stop at first non-empty
                            }
                        }
                    }
                });

                $("#model-title").text(response.title);
                $("#model-description").html(response.description+" uploaded by "+response.creator);
                $("#model-pending").html(response.description?"":"DRAFT (needs version to be searchable)");
                $("#model-quality").html(`
                     <svg class="quality-circle" viewBox="0 0 36 36">
                      <circle cx="18" cy="18" r="18" fill="none" stroke="var(--bg-tertiary)" stroke-width="3"/>
                      <circle cx="18" cy="18" r="18" fill="none" stroke="${response.quality>0.7?'var(--green-primary)':response.quality>0.4?'var(--yellow-primary)':'#F87F76'}" stroke-width="3"
                        stroke-dasharray="100" stroke-dashoffset="${100 - Math.round(response.quality * 100)}"/>
                      <text x="18" y="14" class="quality-text"> ${Math.round(response.quality * 100)}%</text>
                      <text x="18" y="24" class="quality-text">info</text>
                    </svg>
                `);
                const $historyContainer = $("#history-dropdown");
                $historyContainer.html(''); // clear previous content
                if (response.history) {
                    renderHistoryGraph(
                        response.history,
                        Number(id),
                        $historyContainer[0]
                    );
                }
                $("#saveJson").find('.btn-text').hide();
                $("#saveJson").find('.btn-confirmation').fadeIn();
                _renderSimple(true);

                // Restore after 2s
                setTimeout(function () {
                    $("#saveJson").find('.btn-confirmation').fadeOut(function () {
                        $("#saveJson").find('.btn-text').fadeIn();
                        $("#saveJson").fadeOut();
                        //$('#saveJson').attr("disabled", false)
                    });
                }, 1500);
            },
            error: error_handler
        });
    });

    const downloadBtn = document.getElementById("downloadCard");
    const downloadMenu = document.getElementById("downloadDropdown");

    $(downloadBtn).on("click", function() {
        const isOpen = downloadMenu.style.display === "block";
        downloadMenu.style.display = isOpen ? "none" : "block";
        if(isOpen) return;
        const closeMenu = (event) => {
            if(downloadBtn.contains(event.target)) return;
            if(downloadMenu.contains(event.target)) return;
            downloadMenu.style.display = "none";
            document.removeEventListener("click", closeMenu);
        }
        $(document).on("click", closeMenu);
    });

    $(downloadMenu).on("click", e => {
        downloadMenu.style.display = "none";
        const item = e.target.closest(".download-dropdown-item");
        const format = item.getAttribute("data-format");
        const url = "/transparency/card/" + id + "/download/" + format
        $.ajax({
            url: url,
            method: "GET",
            success: function (response) {window.location = url},
            error: error_handler
        });
    });

    const assistBtn = document.getElementById("assistCard");
    const assistMenu = document.getElementById("assistDropdown");
    $(assistBtn).on("click", function() {
        const isOpen = assistMenu.style.display === "block";
        assistMenu.style.display = isOpen ? "none" : "block";
        if(isOpen) return;
        const closeMenu = (event) => {
            if(assistBtn.contains(event.target)) return;
            if(assistMenu.contains(event.target)) return;
            assistMenu.style.display = "none";
            document.removeEventListener("click", closeMenu);
        };
        $(document).on("click", closeMenu);
    });
    $(assistMenu).on("click", function(e) {
        const item = e.target.closest(".download-dropdown-item, .modal_autocomplete, .modal_refine");
        if(!item) return;
        assistMenu.style.display = "none";
        if(item.classList.contains("modal_autocomplete")) $('#modal-autocomplete-screen').css('display' , 'flex');
        else if(item.classList.contains("modal_refine")) $('#modal-refine-screen').css('display' , 'flex');
    });

    $("#cardClone").click(function () {
        if(!token) {
            error_message("You must be logged in to clone a card. Either your session expired or the service temporarily became unavailable, and you need to log in again.");
            return;
        }
        $("#cardClone").prop("disabled", true).text("Cloning...");
        $.ajax({
            url: "/transparency/card/" + id + "/clone",
            method: "POST",
            contentType: "application/json",
            headers: { "Authorization": "Bearer " + token },
            success: function (newId) {window.location.href = "model_card.html?id=" + newId;},
            error: function (xhr, status, error) {
                $("#cardClone").prop("disabled", false).text("Clone");
                error_handler(xhr, status, error);
            }
        });
    });

    $("#modal_autocomplete").click(function () {$('#modal-autocomplete-screen').css('display' , 'flex');});
    $("#modal_refine").click(function () { $('#modal-refine-screen').css('display' , 'flex');});
    $("#deleteCard").click(function () {$('#delete-confirm-screen').css('display' , 'flex');});
    $("#reportCard").click(function () {$('#report-confirm-screen').css('display' , 'flex');});
    $(".delete-confirm-screen").click(function (e) { if ($(e.target).is(this)) $(this).hide();});
    $('#confirm-delete-btn').on('click' , function () {
        $('#delete-confirm-screen').css('display' , 'none');
        $.ajax({
            url: "/transparency/card/" + id, // replace id
            method: "DELETE",
            headers: {"Authorization": "Bearer " + token},
            success: function (response) {
                const screen = $('#delete-success-screen');
                screen.css('display' , 'flex');
                $('#close-success-btn').on('click', function () { screen.css('display' , 'none')});
            },
            error: error_handler
        });
    });
    $('#confirm-report-btn').on('click', function () {
        $('#report-confirm-screen').css('display', 'none');
        $.ajax({
            url: "/transparency/card/" + id + "/report", // report card id
            method: "POST",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify($("#report-text").val()),
            headers: {"Authorization": "Bearer " + token},
            success: function (response) {
                const screen = $('#report-success-screen');
                screen.css('display' , 'flex');
                $('#report-success-btn').on('click', function () { screen.css('display', 'none')});
            },
            error: error_handler
        });
    });

    $(document).on("click", ".card-button", function () {
        if ($(this).parents('#modal-refine-screen').length) {
            const assistant = $(this).attr("id");
            $('#modal-refine-screen').css('display' , 'none');
            $.ajax({
                url: "/transparency/card/" + id + "/clone",
                method: "POST",
                headers: { "Authorization": "Bearer " + token },
                success: function (newId) {
                    runRefinement('agent', newId);
                    window.open("model_card.html?id=" + newId, "_blank");
                }
            });
            return;
        }
        else if ($(this).attr('data-type')==='pdf' || $(this).attr('data-type')==='url') {
            let assistant = $(this).attr("id");
            $("#saveJson").find('.btn-confirmation').fadeOut();
            $.ajax({
                url: "/transparency/card/" + id,
                method: "PUT",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify(cardJson.data.filter(section => section.name !== "history")),
                headers: {"Authorization": "Bearer " + token},
                success: function (response) {
                    $('.menu').find('div').find('.light').removeClass('arrow');
                    $('.menu').find('div').find('.light').addClass('square');

                    ["overview", "use", "training", "evaluation", "performance", "safety"].forEach((sectionName, index) => {
                        let section = cardJson.data.filter(section => section.name !== "history").find(s => s.name === sectionName);
                        let hasValue = false;

                        if (section && section.value) {
                            for (let field of section.value) {
                                if ((field.value.trim() !== "") && (field.value.trim() !== "<br>") && (field.value.trim() !== "unknown")) {
                                    hasValue = true;
                                    $('.menu').find('div').eq(index).find('.light').removeClass('square');
                                    $('.menu').find('div').eq(index).find('.light').addClass('arrow');
                                    break; // stop at first non-empty
                                }
                            }
                        }
                    });

                    if ($('#card-url').is(":visible")) {

                        $.ajax({
                            url: "/transparency/assistant/" + assistant + '/complete/' + id,
                            method: "POST",
                            contentType: "application/json",
                            dataType: "json",
                            headers: { "Authorization": "Bearer " + token},
                            data: JSON.stringify({
                                type: "url",
                                payload: $('#card-url').val()
                            }),
                            success: function (response) {
                                $('#modal-autocomplete-screen').hide();
                                interval = setInterval(function () {checkLocked(interval);}, 300);
                            },
                            error: function (xhr, status, error) {
                                $('#modal-autocomplete-screen').hide();
                                error_handler(xhr, status, error);
                            }
                        });
                    } else {
                        $.ajax({
                            url: "/transparency/assistant/" + assistant + '/complete/' + id,
                            method: "POST",
                            headers: {
                                "Authorization": "Bearer " + token
                            },
                            data: JSON.stringify({
                                type: "html",
                                payload: uploaded_file
                            }),
                            dataType: "json",
                            contentType: "application/json",
                            success: function (response) {
                                $('#modal-autocomplete-screen').hide();
                                interval = setInterval(function () {checkLocked(interval);}, 300);
                                //alert(response)
                            },
                            error: function (xhr, status, error) {
                                $('#modal-autocomplete-screen').hide();
                                error_handler(xhr, status, error);
                            }
                        });
                    }
                },
                error: function (xhr, status, error) {
                    $('#modal-autocomplete-screen').hide();
                    error_handler(xhr, status, error);
                }
            });
        }
    });

    function render_emissions_flash(){
        setTimeout(() => {
            if (token) {
                $.ajax({
                    url: "/transparency/emissions/" + id + '/flash',
                    method: "GET",
                    contentType: "application/json",
                    dataType: "json",
                    headers: {"Authorization": "Bearer " + token},
                    success: function (response) {
                        let energy_consumed = response['energy_consumed'];
                        let emissions = response['emissions'];

                        if (energy_consumed && emissions) {
                            energy_consumed = formatKWh(energy_consumed);
                            emissions = formatKg(emissions);

                            const text = `Job finished with energy consumed ${energy_consumed} and CO2 emissions ${emissions}`;

                            showFlash(text);
                        }
                    },
                    error: error_handler
                });
            }
        }, 2000);
    }

    function showFlash(text) {
        const $container = $("#flash-container");
        const $flash = $("<div>")
            .addClass("flash-message show")
            .html(`
                <span class="close" onclick="this.parentElement.classList.remove('show');setTimeout(() => this.parentElement.remove(), 250);">×</span>
                ${text}
            `);

        $container.append($flash);

        // setTimeout(() => {
        //     flash.classList.remove("show");

        //     setTimeout(() => {
        //         flash.remove();
        //     }, 250);
        // }, 5000); // auto close after 5 sec
    }

    function formatKWh(kWh) {
        const wh = kWh * 1000;
        const units = [
            { name: 'TWh', factor: 1e12 },
            { name: 'GWh', factor: 1e9 },
            { name: 'MWh', factor: 1e6 },
            { name: 'kWh', factor: 1e3 },
            { name: 'Wh',  factor: 1 },
            { name: 'mWh', factor: 1e-3 },
            { name: 'μWh', factor: 1e-6 },
            { name: 'nWh', factor: 1e-9 },
            { name: 'pWh', factor: 1e-12 }
        ];

        let bestUnit = units[units.length - 1]; // fallback to smallest
        let bestValue = wh / bestUnit.factor;

        for (const unit of units) {
            const value = wh / unit.factor;
            if (value >= 1 && value < 1000) {
            bestUnit = unit;
            bestValue = value;
            break;
            }
        }

        const formattedNumber = (Math.abs(bestValue - Math.round(bestValue)) < 1e-10)
            ? Math.round(bestValue).toString()
            : bestValue.toFixed(2).replace(/\.?0+$/, '');

        return `${formattedNumber} ${bestUnit.name}`;
    }

    function formatKg(kg) {
        const grams = kg * 1000;
        const units = [
            { name: 'Mt',   factor: 1e12 },
            { name: 'kt',   factor: 1e9 },
            { name: 't',    factor: 1e6 },
            { name: 'kg',   factor: 1e3 },
            { name: 'g',    factor: 1 },
            { name: 'mg',   factor: 1e-3 },
            { name: 'μg',   factor: 1e-6 },
            { name: 'ng',   factor: 1e-9 }
        ];

        let bestUnit = units[units.length - 1];
        let bestValue = grams / bestUnit.factor;

        for (const unit of units) {
            const value = grams / unit.factor;
            if (value >= 1 && value < 1000) {
            bestUnit = unit;
            bestValue = value;
            break;
            }
    }

    const formatted = (Math.abs(bestValue - Math.round(bestValue)) < 1e-10)
        ? Math.round(bestValue).toString()
        : bestValue.toFixed(2).replace(/\.?0+$/, '');
    return `${formatted} ${bestUnit.name}`;
    }

    // ignore text/html when pasting to a field
    $(document).on("paste", ".field-value[contenteditable='true']", function (e) {
        e.preventDefault();
        const text = (e.originalEvent || e).clipboardData.getData("text/plain");
        document.execCommand("insertText", false, text);
    });
});

