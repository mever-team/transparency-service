

$(function () {
    $('#loading').show();
    $("#topic").val(localStorage.getItem("last_search_term") || "");
    $("#topic").trigger("keyup");
    if(localStorage.getItem('modalDismissed') !== 'true') $('.modal__trigger[data-modal="#modal_help"]').click();
    $('body').on('click', '.demo-close', ()=>{localStorage.setItem('modalDismissed', 'true');});
    $("#username, #password").on("keydown", (e)=>{
        if ((e.key && e.key !== "Enter") && e.which !== 13 && e.keyCode !== 13) return;
        e.preventDefault();
        $("#login-confirm-btn").trigger("click");
    });
    $("#register-username, #register-password, #register-password-verify, #register-email").on("keydown", (e)=>{
        if ((e.key && e.key !== "Enter") && e.which !== 13 && e.keyCode !== 13) return;
        e.preventDefault();
        $("#register-confirm-btn").trigger("click");
    });
    $('#login-btn').click(() => { $('#login-error').text(""); $('#login').addClass('show'); });
    $('#cancel-login-btn').click(() => { $('#login-error').text(""); $('#login').removeClass('show'); });
    $('#register-btn').click(() => { $('#register-error').text("");$('#register-success').text(""); $('#register').addClass('show'); });
    $('#cancel-register-btn').click(() => { $('#register-success').text("");$('#register-error').text(""); $('#register').removeClass('show'); });
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
    $('#register-confirm-btn').click(() => {
        const username = $('#register-username').val().trim();
        const email = $('#register-email').val().trim();
        const password = $('#register-password').val();
        const verify = $('#register-password-verify').val();
        $('#register-error').text("");
        $('#register-success').text("");
        if (!username || !email || !password || !verify) {
            $('#register-error').text("All fields are required.");
            return;
        }
        if (password !== verify) {
            $('#register-error').text("Passwords do not match.");
            return;
        }
        $.ajax({
            url: '/transparency/register',
            method: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({
                username: username,
                email: email,
                password: password
            }),
            success: function () {
                //$('#register').removeClass('show');
                $('#register-success').addClass('show');
                $('#register-success').text("Your account is pending administrator approval.");
            },
            error: function (xhr) {
                if (xhr.responseJSON && xhr.responseJSON.error) $('#register-error').text(xhr.responseJSON.error);
                else if (xhr.responseText) $('#register-error').text(xhr.responseText);
                else $('#register-error').text("Registration failed");
            }
        });
    });

});


$('#login-confirm-btn').click(()=>{
    $.ajax({
        url: '/transparency/login',
        method: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({username: $('#username').val(), password: $('#password').val()}),
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