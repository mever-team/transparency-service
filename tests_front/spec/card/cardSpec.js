let karmaTestCardId = undefined;
describe('Testing card.html...', function() {
    beforeAll(async function () {
        /* create a card */
        karmaTestCardId = await createCard('admin', 'admin');
        let url = '/base/ui/transparency/model_card.html'
        await loadPage(url, asAdmin = true);
    });
    // afterAll(function(){
    //     document.cookie = "access_token=; path=/; max-age=0;"
    //     token = '';
    // });


    it('Testing something idk', async function(){
        expect($('#modal-autocomplete-screen').is(':visible')).toBe(true);
        expect($('#model-description').text()).toBe(' uploaded by admin');
    });

})