describe('Testing filters...', function() {
    let iframe;
    let iframeDoc;

    beforeEach(function(done) {
        iframe = document.createElement('iframe');
        iframe.src = '/transparency/index.html';
        document.body.appendChild(iframe);

        iframe.onload = function() {
            // make sure all dynamic elements are loaded
            setTimeout(() => {
            iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                done();
            }, 5000);
        };
    });

    afterEach(function() {
        iframe.remove();
    });

    it('Open filter modal', function() {
        $(iframeDoc).find("#new-filter").trigger('click');
        $modal = $(iframeDoc).find(".modal.modal__bg#filters");
        expect($modal.hasClass('modal--active')).toBe(true);
    });
});