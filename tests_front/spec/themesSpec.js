describe('Testing themes...', function() {
    let iframe;
    let iframeDoc;

    beforeEach(function(done) {
        iframe = document.createElement('iframe');
        iframe.src = '/transparency/account.html';
        document.body.appendChild(iframe);

        iframe.onload = function() {
            iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
            done();
        };
    });

    afterEach(function() {
        iframe.remove();
    });

    it('Testing light theme', function(){
        iframe.contentWindow.setTheme('light-theme');
        expect(iframe.contentWindow.localStorage.getItem('theme')).toBe('light-theme');
        
    });

    it('Testing dark theme', function(){
        iframe.contentWindow.setTheme('dark-theme');
        expect(iframe.contentWindow.localStorage.getItem('theme')).toBe('dark-theme');
    });

    it('Testing ocean theme', function(){
        iframe.contentWindow.setTheme('ocean-theme');
        expect(iframe.contentWindow.localStorage.getItem('theme')).toBe('ocean-theme');
    });

})