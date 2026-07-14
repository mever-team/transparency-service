describe('Testing themes...', function() {
    beforeAll(async function () {
        await loadPage('/base/ui/transparency/index.html');
    });


    it('Testing light theme', function(){
        setTheme('light-theme');
        expect(localStorage.getItem('theme')).toBe('light-theme');
        
    });

    it('Testing dark theme', function(){
        setTheme('dark-theme');
        expect(localStorage.getItem('theme')).toBe('dark-theme');
    });

    it('Testing ocean theme', function(){
        setTheme('ocean-theme');
        expect(localStorage.getItem('theme')).toBe('ocean-theme');
    });

})