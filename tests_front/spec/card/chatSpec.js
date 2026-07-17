describe('Testing chat.js...', function() {
    beforeAll(async function () {
        /* create a card */
        karmaTestCardId = await createCard('admin', 'admin');
        let url = '/base/ui/transparency/model_card.html';
        await loadPage(url, asAdmin = true);
    });

    it('Testing chat Open and close with buttons', function(){
        expect($("#ai-chat-overlay").hasClass('active')).toBe(false);
        $("#ai-chat-trigger").trigger('click');
        expect($("#ai-chat-overlay").hasClass('active')).toBe(true);
        $("#ai-chat-close").trigger('click');
        expect($("#ai-chat-overlay").hasClass('active')).toBe(false);
    });
    
    it('Testing chat Open with button and close with click', function(){
        $("#ai-chat-trigger").trigger('click');
        expect($("#ai-chat-overlay").hasClass('active')).toBe(true);
        $("#ai-chat-overlay").trigger('click');
        expect($("#ai-chat-overlay").hasClass('active')).toBe(false);
    });
    
    it('Testing chat Send a message to trai', async function(){
        $('#ai-chat-input').val('hello from karma');
        $('#ai-chat-input').trigger($.Event('keydown', {
            key: 'Enter',
            code: 'Enter',
            keyCode: 13,
            which: 13
        }));
        await wait4ajax();
        expect($('.ai-msg.assistant').length).not.toBe(0);
        expect($('.ai-msg.user').length).not.toBe(0);
    });

})