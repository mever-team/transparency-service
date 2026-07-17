describe('Testing handbook...', function() {
    beforeAll(async function () {
        await loadPage('/base/ui/transparency/handbook.html');
    });
    afterAll(function(){
        cleanupHandbookScrollHandler();
    });


    it('Testing scrolls and hide/show menu', async function(){
        handbookBodyElement = document.getElementById("handbookBody");
        const bodyIds = Array.from(handbookBodyElement.querySelectorAll('[id]')).map(el => el.id);
        await window.scrollTo(0, 0);
        expect(window.scrollY).toBe(0);
        handbookGoTo(bodyIds[1]);
        await new Promise(resolve => setTimeout(resolve, 1000));
        expect(window.scrollY).not.toBe(0);

        expect($('#handbookMenu').find('div').is(':visible')).toBe(true)
        $('#hideMenuBtn').trigger('click');
        await wait4animations();
        expect($('#handbookMenu').find('div').is(':visible')).toBe(false)
        $('#hideMenuBtn').trigger('click');
        await wait4animations();
        expect($('#handbookMenu').find('div').is(':visible')).toBe(true)
    });

})