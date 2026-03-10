$(function () {
    $('#loading').show();
    $("#topic").trigger("keyup");
    if(localStorage.getItem('modalDismissed') !== 'true') $('.modal__trigger[data-modal="#modal_help"]').click();
    $('body').on('click', '.demo-close', ()=>{localStorage.setItem('modalDismissed', 'true');});
    $("#username,#password,#email").on("keydown", (e)=>{
        if (!$('#username').is(':visible')) return;
        if ((e.key && e.key !== "Enter") && e.which !== 13 && e.keyCode !== 13) return;
        e.preventDefault();
        $("#login-confirm-btn").trigger("click");
    });
    let cancelLogin = () => { $('#login-error').text(""); $('#login').removeClass('show'); }
    $('#login-btn').click(() => { $('#login-error').text(""); $('#login').addClass('show'); });
    $('#cancel-login-btn').click(cancelLogin);
    $('#account-btn').click(() => { window.location.href = 'account.html'; });
    $('#new_card').click(() => {
        $.ajax({
            url: "/transparency/card",
            method: "POST",
            contentType: "application/json",
            headers: { "Authorization": "Bearer " + token },
            data: JSON.stringify({ title: "" }),
            success: r => window.location.href = 'model_card.html?id=' + r,
            error: () => alert("Failed to create a new model card. Please refresh the page and try again.")
        });
    });
    $(document).on('keydown', (e) => {
      if(e.key !== 'Escape') return;
      if($('#login').hasClass('show')) cancelLogin();
    });
});

$('#login_password').click(function () {
    $('#password_label').slideUp();
    $('#email_label').slideDown();
});

$('#login_email').click(function () {
    $('#password_label').slideDown();
    $('#email_label').slideUp();
});

$('#login-confirm-btn').click(()=>{
    let username = $('#username').val();
    if(!username)
        return;
    let password = $('#password').val();
    let email = $('#email').val();
    if ($('#email').is(':visible')) {
        $.ajax({
            url: '/transparency/register',
            method: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({username: username, email: email, password: ""}),
            success: function () {
                $('#login-error').text("");
                //$('#register').removeClass('show');
                $('#login-success').addClass('show');
                $('#login-success').text("An email was sent to your account with a login link. Check your spam folder.");
            },
            error: function (xhr) {
                $('#login-success').text("");
                if (xhr.responseJSON && xhr.responseJSON.error) $('#login-error').text(xhr.responseJSON.error);
                else if (xhr.responseText) $('#login-error').text(xhr.responseText);
                else $('#login-error').text("Registration failed");
            }
        });
        return;
    }
    $.ajax({
        url: '/transparency/login',
        method: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({username: username, password: password}),
        success: function (response) {
            token = response.token;
            updateUsername();
            $('#login').removeClass('show');
        },
        error: function (xhr) {
            token = '';
            updateUsername();
            if (xhr.responseJSON && xhr.responseJSON.error) $('#login-error').text('Failed to login: ' + xhr.responseJSON.error);
            else $('#login-error').text('Server is offline');
        }
    });
});

$('.modal__trigger').on('click', function () {
    const target = $(this).data('modal');
    $(target)
        .addClass('modal--active')
        .find('.modal__content')
        .addClass('modal__content--active');
});
$('.modal-close').on('click', function () {
    $(this).closest('.modal')
        .removeClass('modal--active')
        .find('.modal__content')
        .removeClass('modal__content--active');
});
$('.modal').on('click', function (e) {
    if (e.target !== this) return;
    $(this)
        .removeClass('modal--active')
        .find('.modal__content')
        .removeClass('modal__content--active');
});

