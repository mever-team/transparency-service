describe('Testing account.html...', function() {
    beforeEach(async function () {
        await loadPage('/base/ui/transparency/account.html', asAdmin = true);
    });


    it('Testing change theme', async function(){
        $('#theme-selector').val('light-theme').change();
        expect($('body').hasClass('dark-theme')).toBe(false);
        $('#theme-selector').val('dark-theme').change();
        expect($('body').hasClass('dark-theme')).toBe(true);
    });

    it('Testing accept reject pending user', async function(){
        await registerUser('karma-accept', 'karma-accept@example.com');
        await registerUser('karma-reject', 'karma-reject@example.com');
        await loadPage('/base/ui/transparency/account.html', asAdmin = true);
        expect($('#pending-users .pending-btn[data-username="karma-accept"]').length).toBe(1);
        $('#pending-users .pending-btn[data-username="karma-accept"]').trigger('click');
        await wait4ajax();
        expect($('#pending-users .delete-btn[data-username="karma-reject"]').length).toBe(1);
        spyOn(window, 'confirm').and.returnValue(true);
        $('#pending-users .delete-btn[data-username="karma-reject"]').trigger('click');
        await wait4ajax();
        await loadPage('/base/ui/transparency/account.html', asAdmin = true);
        expect($('#registered-users .delete-btn[data-username="karma-accept"]').length).toBe(1);
        expect($('#registered-users .delete-btn[data-username="karma-reject"]').length).toBe(0);
        $('#registered-users .delete-btn[data-username="karma-accept"]').trigger('click');
        await wait4ajax();
        await loadPage('/base/ui/transparency/account.html', asAdmin = true);
        expect($('#registered-users .delete-btn[data-username="karma-accept"]').length).toBe(0);
    });

    it('Testing change password', async function(){
        /* Deny admin change through API */
        $('#password').val('badpwd');
        $('#password-verify').val('badpwd');
        $('#confirm-password-btn').trigger('click');
        await wait4ajax();
        expect($('#password-error').text()).toBe('Administrator password cannot be modified via API');

        /* Do not match */
        $('#password').val('badpwd');
        $('#password-verify').val('anotherbadpwd');
        $('#confirm-password-btn').trigger('click');
        expect($('#password-error').text()).toBe('The new password does not match its verification.');

        /* empty password */
        $('#password').val('');
        $('#password-verify').val('');
        $('#confirm-password-btn').trigger('click');
        expect($('#password-error').text()).toBe('Provide a new password.');
    });

    it('Testing modals', async function(){
        $('#cancel-report-btn').trigger('click');
        expect($('#cancel-report-btn').is(':visible')).toBe(false);
        $('#report-modal-screen').show();
        expect($('#cancel-report-btn').is(':visible')).toBe(true);
        $('#cancel-report-btn').trigger('click');
        expect($('#cancel-report-btn').is(':visible')).toBe(false);

        $('#cancel-password-btn').trigger('click');
        expect($('#password-modal-screen').is(':visible')).toBe(false);
        $('#password-open-btn').trigger('click');
        expect($('#password-modal-screen').is(':visible')).toBe(true);
        $('#cancel-password-btn').trigger('click');
        expect($('#password-modal-screen').is(':visible')).toBe(false);
    });


})