describe('Testing index main.js...', function() {
    beforeEach(async function () {
        await loadPage('/base/ui/transparency/index.html');
    });

    it('login logout', async function() {
        $('#login-btn').trigger('click');
        expect($('#login').hasClass('show')).toBe(true);
        /* Check email slide */
        $('#login_password').trigger('click');
        await wait4animations();
        expect($('#password_label').is(':visible')).toBe(false);
        expect($('#email_label').is(':visible')).toBe(true);
        $('#login_email').trigger('click');
        await wait4animations();
        expect($('#password_label').is(':visible')).toBe(true);
        expect($('#email_label').is(':visible')).toBe(false);
        /* login */
        $('#username').val('admin');
        $('#password').val('admin');
        // $('#login-confirm-btn').trigger('click');
        $('#password').trigger($.Event('keydown', {
            key: 'Enter',
            code: 'Enter',
            keyCode: 13,
            which: 13
        }));
        await wait4ajax();
        expect($('#account-name').text()).toBe('admin');
        $('#logout-btn').trigger('click');
        await wait4ajax();
        expect($('#account-name').text()).toBe('admin');
    });

    it('register', async function() {
        $('#login_password').trigger('click');
        await wait4animations();
        expect($('#password_label').is(':visible')).toBe(false);
        expect($('#email_label').is(':visible')).toBe(true);
        $('#username').val('karma');
        $('#email').val('karma@example.com');
        $('#login-confirm-btn').trigger('click');
        await wait4ajax();
        expect($('#login-success').text()).toBe('An email was sent to your account with a login link. Check your spam folder.');
    });


    it('modal triggers', function() {
        expect($('.modal#help').hasClass('modal--active')).toBe(false);
        $('.modal__trigger#whats-this').trigger('click');
        expect($('.modal#help').hasClass('modal--active')).toBe(true);
        $('.modal-close').trigger('click');
        expect($('.modal#help').hasClass('modal--active')).toBe(false);

        expect($('.modal#filters').hasClass('modal--active')).toBe(false);
        $('.modal__trigger#new-filter').trigger('click');
        expect($('.modal#filters').hasClass('modal--active')).toBe(true);
        $('.modal#filters').trigger('click');
        expect($('.modal#filters').hasClass('modal--active')).toBe(false);
    });

});