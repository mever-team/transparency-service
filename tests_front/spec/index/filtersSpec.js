describe('Testing filters...', function() {
    beforeEach(async function () {
        await loadPage('/base/ui/transparency/index.html');
    });

    it('Set & remove a Task filter', function() {
        /* Open filter modal */
        $("#new-filter").trigger('click');
        $modal = $(".modal.modal__bg#filters");
        expect($modal.hasClass('modal--active')).toBe(true);

        /* Select a 'Task' filter */
        document.getElementById('filter-select').value = 'task';
        document.getElementById('filter-select').dispatchEvent(new Event("change", { bubbles: true }));
        $('.filter-option[data-filter="Audio-Text-to-Text"]').trigger('click');
        expect($('.filter-option[data-filter="Audio-Text-to-Text"]').hasClass('active')).toBe(true);

        /* Trigger done and check caption */
        $('.filter-done').trigger('click');
        $taskFilterCaption = $('#edit-filter[data-filter="task"]');
        expect($taskFilterCaption.html()).toContain('Audio‑Text‑to‑Text');

        /* Edit filter */
        $taskFilterCaption.trigger('click');
        $modal = $(".modal.modal__bg#filters");
        expect($modal.hasClass('modal--active')).toBe(true);
        $('.filter-option[data-filter="Image-Text-to-Text"]').trigger('click');
        $('.filter-done').trigger('click');
        $taskFilterCaption = $('#edit-filter[data-filter="task"]');
        expect($taskFilterCaption.html()).toContain('Image‑Text‑to‑Text');

        /* Remove Task filter and check caption */
        $taskFilterCaption.find('.remove-filter').trigger('click');
        $taskFilterCaption = $('#edit-filter[data-filter="task"]');
        expect($taskFilterCaption.html()).toBe(undefined);
    });

    it('Set & remove a Type filter', function() {
        /* Open filter modal */
        $("#new-filter").trigger('click');
        $modal = $(".modal.modal__bg#filters");
        expect($modal.hasClass('modal--active')).toBe(true);

        /* Select a 'Type' filter */
        document.getElementById('filter-select').value = 'type';
        document.getElementById('filter-select').dispatchEvent(new Event("change", { bubbles: true }));
        $('.filter-option[data-filter="Convolutional Neural Network"]').trigger('click');
        expect($('.filter-option[data-filter="Convolutional Neural Network"]').hasClass('active')).toBe(true);

        /* Trigger done and check caption */
        $('.filter-done').trigger('click');
        $typeFilterCaption = $('#edit-filter[data-filter="type"]');
        expect($typeFilterCaption.html()).toContain('Convolutional&nbsp;Neural&nbsp;Network');

        /* Edit filter */
        $typeFilterCaption.trigger('click');
        $modal = $(".modal.modal__bg#filters");
        expect($modal.hasClass('modal--active')).toBe(true);
        $('.filter-option[data-filter="Recurrent Neural Network"]').trigger('click');
        $('.filter-done').trigger('click');
        $typeFilterCaption = $('#edit-filter[data-filter="type"]');
        expect($typeFilterCaption.html()).toContain('Recurrent&nbsp;Neural&nbsp;Network');

        /* Remove Type filter and check caption */
        $typeFilterCaption.find('.remove-filter').trigger('click');
        $typeFilterCaption = $('#edit-filter[data-filter="type"]');
        expect($typeFilterCaption.html()).toBe(undefined);
    });

    it('Set & remove a Info filter', function() {
        /* Open filter modal */
        $("#new-filter").trigger('click');
        $modal = $(".modal.modal__bg#filters");
        expect($modal.hasClass('modal--active')).toBe(true);

        /* Select a 'Info' filter */
        document.getElementById('filter-select').value = 'info';
        document.getElementById('filter-select').dispatchEvent(new Event("change", { bubbles: true }));
        $('.info-input').val(10).trigger("input");
        expect($('.info-input').val()).toBe('10');

        /* Trigger done and check caption */
        $('.filter-done').trigger('click');
        $infoFilterCaption = $('#edit-filter[data-filter="info"]');
        expect($infoFilterCaption.html()).toContain('10&nbsp;%');

        /* Edit filter */
        $infoFilterCaption.trigger('click');
        $modal = $(".modal.modal__bg#filters");
        expect($modal.hasClass('modal--active')).toBe(true);
        $('.info-input').val(20).trigger("input");
        expect($('.info-input').val()).toBe('20');
        $('.filter-done').trigger('click');
        $infoFilterCaption = $('#edit-filter[data-filter="info"]');
        expect($infoFilterCaption.html()).toContain('20&nbsp;%');

        /* Remove Task filter and check caption */
        $infoFilterCaption.find('.remove-filter').trigger('click');
        $infoFilterCaption = $('#edit-filter[data-filter="info"]');
        expect($infoFilterCaption.html()).toBe(undefined);
    });

    it('Type in seachbar', function(done) {
        resultsBefore = $('#resultsTable').html()
        $('input#topic').val('hi').trigger("keyup");
        setTimeout(() => {// wait for trai to respond
            resultsAfter = $('#resultsTable').html()
            expect(resultsBefore).not.toBe(resultsAfter);
            done();
        }, 1000);
    });

});