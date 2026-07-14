let loaded = [];
describe('Testing filters...', function() {
    beforeAll(async function () {
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
});