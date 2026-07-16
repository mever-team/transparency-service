describe('Testing card.js...', function() {
    beforeEach(async function () {
        /* create a card */
        karmaTestCardId = await createCard('admin', 'admin');
        let url = '/base/ui/transparency/model_card.html';
        await loadPage(url, asAdmin = true);
    });


    it('Testing layout visibilities', async function(){
        /* Initial layout */
        expect($('#modal-autocomplete-screen').is(':visible')).toBe(true);
        expect($('#model-description').text()).toBe(' uploaded by admin');

        /* .menu visibility */
        expect($('.menu').hasClass('active')).toBe(false);
        $('#technical-view').trigger('click');
        expect($('.menu').hasClass('active')).toBe(true);

        /* #assistDropdown visibility */
        expect($('#assistDropdown').is(':visible')).toBe(false);
        $('#assistCard').trigger('click');
        expect($('#assistDropdown').is(':visible')).toBe(true);
        $('body').trigger('click');
        expect($('#assistDropdown').is(':visible')).toBe(false);

        /* #downloadDropdown visibility */
        expect($('#downloadDropdown').is(':visible')).toBe(false);
        $('#downloadCard').trigger('click');
        expect($('#downloadDropdown').is(':visible')).toBe(true);
        $('body').trigger('click');
        expect($('#assistDropdown').is(':visible')).toBe(false);

        /* modals visibility */
        // import
        $('#cancel-autocomplete-btn').trigger('click');
        expect($('#modal-autocomplete-screen').is(':visible')).toBe(false);
        $('#import-btn').trigger('click');
        expect($('#modal-autocomplete-screen').is(':visible')).toBe(true);
        $('#modal-autocomplete-screen').trigger('click');
        expect($('#modal-autocomplete-screen').is(':visible')).toBe(false);
        // refine
        expect($('#modal-refine-screen').is(':visible')).toBe(false);
        $('.download-dropdown-item.modal_refine').trigger('click');
        expect($('#modal-refine-screen').is(':visible')).toBe(true);
        $('#modal-refine-screen').trigger('click');
        expect($('#modal-refine-screen').is(':visible')).toBe(false);
        $('.download-dropdown-item.modal_refine').trigger('click');
        expect($('#modal-refine-screen').is(':visible')).toBe(true);
        $('#cancel-refine-btn').trigger('click');
        expect($('#modal-refine-screen').is(':visible')).toBe(false);
        // delete
        expect($('#delete-confirm-screen').is(':visible')).toBe(false);
        $('#deleteCard').trigger('click');
        expect($('#delete-confirm-screen').is(':visible')).toBe(true);
        $('#cancel-delete-btn').trigger('click');
        expect($('#delete-confirm-screen').is(':visible')).toBe(false);
        $('#deleteCard').trigger('click');
        expect($('#delete-confirm-screen').is(':visible')).toBe(true);
        $('#delete-confirm-screen').trigger('click');
        expect($('#delete-confirm-screen').is(':visible')).toBe(false);
        // espace behaviour
        // TODO: check all modals because esc works for all
        $('#import-btn').trigger('click');
        expect($('#modal-autocomplete-screen').is(':visible')).toBe(true);
        const esc = $.Event("keydown", { key: 'Escape', keyCode: 27 });
        $('body').trigger(esc);
        expect($('#modal-autocomplete-screen').is(':visible')).toBe(false);

        /* content visibility */
        $('#technical-view').trigger('click');
        expect($('ul.nacc li').eq(1).hasClass('active')).toBe(false);
        $('.menu div').eq(1).trigger('click');
        expect($('ul.nacc li').eq(1).hasClass('active')).toBe(true);

        /* import modal layout */
        $('#import-btn').trigger('click');
        $('#pdf_text').trigger('click');
        await new Promise(resolve => setTimeout(resolve, 1000)) // wait for jquery slide
        expect($('#pdf_desc').is(':visible')).toBe(true);
        expect($('#url_desc').is(':visible')).toBe(false);
        expect($('#metrics_desc').is(':visible')).toBe(false);
        $('#url_text').trigger('click');
        await new Promise(resolve => setTimeout(resolve, 1000)) // wait for jquery slide
        expect($('#url_desc').is(':visible')).toBe(true);
        expect($('#pdf_desc').is(':visible')).toBe(false);
        expect($('#metrics_desc').is(':visible')).toBe(false);
        $('#metrics_text').trigger('click');
        await new Promise(resolve => setTimeout(resolve, 1000)) // wait for jquery slide
        expect($('#metrics_desc').is(':visible')).toBe(true);
        expect($('#pdf_desc').is(':visible')).toBe(false);
        expect($('#url_desc').is(':visible')).toBe(false);

        /* Option fields suggetions */
        expect($('.contents input').eq(1).closest('div').find('.autocomplete-suggestions').is(':visible')).toBe(false);
        $('#technical-view').trigger('click');
        $('.contents input').eq(1).focus();
        $('.contents input').eq(1).trigger('focus');
        expect($('.contents input').eq(1).closest('div').find('.autocomplete-suggestions').is(':visible')).toBe(true);

    });

    it('Testing clone card', async function(){
        expect($('#history-dropdown').html()).toBe('');
        $('#cardClone').trigger('click');
        await new Promise(resolve => setTimeout(resolve, 2000)); // wait for trai
        /* Manual redirect */
        karmaTestCardId += 1;
        let url = '/base/ui/transparency/model_card.html'
        await loadPage(url, asAdmin = true);
        expect($('#history-dropdown').html()).not.toBe('');
    });


    it('Testing import', async function(){
        let importURL = 'http://localhost:5000'
        $('#import-btn').trigger('click');
        expect($('.quality-text').html().trim()).toBe('0%');
        $('#card-url').val(importURL);
        $('#modal-autocomplete-screen .card-button[data-type=url]').trigger('click');
        /* Manual reload */
        let assistantRuning = true;
        const maxTries = 5;
        let currentTry = 0;
        while (assistantRuning){
            if (currentTry>maxTries) {
                console.log('Failed to import. Max tries reached')
                expect($('.quality-text').text().trim()).not.toBe('0%');
                break;
            }
            await new Promise(resolve => setTimeout(resolve, 5000)); // wait for trai to import
            let url = '/base/ui/transparency/model_card.html'
            await loadPage(url, asAdmin = true);
            if ($('.quality-text').text().trim() !== '0%') {
                break;
                assistantRuning = false;
            }
            currentTry+=1;
        }
        expect($('.quality-text').text().trim()).not.toBe('0%');
    });

    it('Testing refine', async function(){
        expect($('#history-dropdown').html()).toBe('');
        $('#modal-refine-screen .card-button').trigger('click');
        /* Manual redirect */
        let assistantRuning = true;
        const maxTries = 20;
        let currentTry = 0;
        karmaTestCardId += 1;
        while (assistantRuning){
            if (currentTry>maxTries) {
                console.log('Failed to refine. Max tries reached')
                expect($('#history-dropdown').html()).not.toBe('');
                 break;
            }
            await new Promise(resolve => setTimeout(resolve, 1000)); // wait for trai to import
            let url = '/base/ui/transparency/model_card.html'
            await loadPage(url, asAdmin = true);
            if ($('#history-dropdown').html() !== '') {
                break;
                assistantRuning = false;
            }
            currentTry+=1;
        }
        expect($('#history-dropdown').html()).not.toBe('');
    });

    it('Testing delete', async function(){
        expect($('#delete-success-screen').is(':visible')).toBe(false);
        $('#confirm-delete-btn').trigger('click');
        await new Promise(resolve => setTimeout(resolve, 2000)) // wait for trai
        expect($('#delete-success-screen').is(':visible')).toBe(true);
    });
    it('save and reload', async function(){
        $('.contents').find('.field-value').first().text('karma-test');
        $('#saveJson').trigger('click');
        await new Promise(resolve => setTimeout(resolve, 1000)) // wait for trai
        /* Manual reload */
        let url = '/base/ui/transparency/model_card.html'
        await loadPage(url, asAdmin = true);
        expect($('.contents').find('.field-value').first().text().trim()).toBe('karma-test');
    });
    it('Testing mediumeditor', function(){
        /* show toolbar */
        expect($('.medium-editor-toolbar.static-toolbar').hasClass('medium-editor-toolbar-active')).toBe(false);
        $('#technical-view').trigger('click');
        $('.contents').find('.field-value').first().focus();
        $('.contents').find('.field-value').first().trigger('click');
        expect($('.medium-editor-toolbar.static-toolbar').hasClass('medium-editor-toolbar-active')).toBe(true);
        expect($('.contents').find('.field-value').first().html()).toBe('');
        /* bond */
        expect($('.medium-editor-action[data-action="bold"]').hasClass('medium-editor-button-active')).toBe(false);
        $('.medium-editor-action[data-action="bold"]').trigger('click');
        expect($('.medium-editor-action[data-action="bold"]').hasClass('medium-editor-button-active')).toBe(true);
        $('.medium-editor-action[data-action="bold"]').trigger('click');
        expect($('.medium-editor-action[data-action="bold"]').hasClass('medium-editor-button-active')).toBe(false);
        /* italic */
        expect($('.medium-editor-action[data-action="italic"]').hasClass('medium-editor-button-active')).toBe(false);
        $('.medium-editor-action[data-action="italic"]').trigger('click');
        expect($('.medium-editor-action[data-action="italic"]').hasClass('medium-editor-button-active')).toBe(true);
        $('.medium-editor-action[data-action="italic"]').trigger('click');
        expect($('.medium-editor-action[data-action="italic"]').hasClass('medium-editor-button-active')).toBe(false);
        /* underline */
        expect($('.medium-editor-action[data-action="underline"]').hasClass('medium-editor-button-active')).toBe(false);
        $('.medium-editor-action[data-action="underline"]').trigger('click');
        expect($('.medium-editor-action[data-action="underline"]').hasClass('medium-editor-button-active')).toBe(true);
        $('.medium-editor-action[data-action="underline"]').trigger('click');
        expect($('.medium-editor-action[data-action="underline"]').hasClass('medium-editor-button-active')).toBe(false);
        // TODO: find out why they don't work
        /* append-blockquote */
        // expect($('.medium-editor-action[data-action="append-blockquote"]').hasClass('medium-editor-button-active')).toBe(false);
        // $('.medium-editor-action[data-action="append-blockquote"]').trigger('click');
        // expect($('.medium-editor-action[data-action="append-blockquote"]').hasClass('medium-editor-button-active')).toBe(true);
        // $('.medium-editor-action[data-action="append-blockquote"]').trigger('click');
        // expect($('.medium-editor-action[data-action="append-blockquote"]').hasClass('medium-editor-button-active')).toBe(false);
        /* insertorderedlist */ 
        // expect($('.medium-editor-action[data-action="insertorderedlist"]').hasClass('medium-editor-button-active')).toBe(false);
        // $('.medium-editor-action[data-action="insertorderedlist"]').trigger('click');
        // expect($('.medium-editor-action[data-action="insertorderedlist"]').hasClass('medium-editor-button-active')).toBe(true);
        // $('.medium-editor-action[data-action="insertorderedlist"]').trigger('click');
        // expect($('.medium-editor-action[data-action="insertorderedlist"]').hasClass('medium-editor-button-active')).toBe(false);
        /* insertunorderedlist */
        // expect($('.medium-editor-action[data-action="insertunorderedlist"]').hasClass('medium-editor-button-active')).toBe(false);
        // $('.medium-editor-action[data-action="insertunorderedlist"]').trigger('click');
        // expect($('.medium-editor-action[data-action="insertunorderedlist"]').hasClass('medium-editor-button-active')).toBe(true);
        // $('.medium-editor-action[data-action="insertunorderedlist"]').trigger('click');
        // expect($('.medium-editor-action[data-action="insertunorderedlist"]').hasClass('medium-editor-button-active')).toBe(false);
        /* Code Block */
        // expect($('.medium-editor-action[title="Code Block"]').hasClass('medium-editor-button-active')).toBe(false);
        // $('.medium-editor-action[title="Code Block"]').trigger('click');
        // expect($('.medium-editor-action[title="Code Block"]').hasClass('medium-editor-button-active')).toBe(true);
        // $('.medium-editor-action[title="Code Block"]').trigger('click');
        // expect($('.medium-editor-action[title="Code Block"]').hasClass('medium-editor-button-active')).toBe(false);
    });

});