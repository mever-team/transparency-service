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
        expect(window.scrollY).toBe(0);
        handbookGoTo(bodyIds[1]);
        await new Promise(resolve => setTimeout(resolve, 1000)); // wait for smooth scroll
        expect(window.scrollY).not.toBe(0);

        expect($('#handbookMenu').find('div').is(':visible')).toBe(true)
        $('#hideMenuBtn').trigger('click');
        await new Promise(resolve => setTimeout(resolve, 1000)); // wait for smooth slide
        expect($('#handbookMenu').find('div').is(':visible')).toBe(false)
        $('#hideMenuBtn').trigger('click');
        await new Promise(resolve => setTimeout(resolve, 1000)); // wait for smooth slide
        expect($('#handbookMenu').find('div').is(':visible')).toBe(true)
    });

})