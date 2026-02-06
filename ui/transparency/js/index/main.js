$(function () {
    $('#loading').show();
    $("#topic").val(localStorage.getItem("last_search_term") || "");
    autocomplete_populate();
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

function autocomplete_populate() {
    let lastUpdate = 0, pending = null, first = true, delay = 150;
    const $topic = $("#topic"), $tbody = $("#resultsTable tbody");
    function request() {
        const q = $topic.val().trim();
        if (first) $('#loading').show();
        $.ajax({
            url: "/transparency/cards",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ query: q }),
            success: r => {
                $('#loading').hide();
                const results = r.results || [];

                $('#search_results_wrapper').text("Showing");
                $('#search_results').text(results.length + " of " + (r.total || 0));
                $tbody.empty();

                if (results.length)
                    results.forEach(it => {
                        const name = it.name.replace(new RegExp("(" + q + ")", "ig"),"<strong style='color:#79CFDC'>$1</strong>");
                        const type = (it.type || it.task || "").toLowerCase();
                        const task = it.task ? " for " + it.task.toLowerCase() : "";
                        $tbody.append(`
<tr class="search_results_button">
<td>
<a style="display:block;width:100%;height:100%;text-decoration:none;text-align:left" href="model_card.html?id=${it.id}">
<div class="row">
<div>
<svg class="quality-circle" viewBox="0 0 36 36">
<circle cx="18" cy="18" r="18" fill="none" stroke="#434343" stroke-width="3"/>
<circle cx="18" cy="18" r="18" fill="none"
stroke="${it.quality>0.7?'#6CC06B':it.quality>0.4?'#FBC483':'#F87F76'}"
stroke-width="3"
stroke-dasharray="100"
stroke-dashoffset="${100 - Math.round(it.quality * 100)}"/>
<text x="18" y="14" class="quality-text">${Math.round(it.quality * 100)}%</text>
<text x="18" y="24" class="quality-text">info</text>
</svg>
</div>
<div>
<span style="display:block;color:#EEE">${name}</span>
<span style="font-size:13px;color:#F9AB49">${it.desc ? "" : "DRAFT (no version)"}</span>
<span style="font-size:13px;color:#79CFDC">${(it.desc || "") + (it.creator ? " by " + it.creator : "")}</span>
<span style="font-size:13px;color:#79CFDC">${type ? " --- " + type + task : ""}</span>
</div>
</div>
<div style="font-size:13px;color:#C8C8C8;margin-top:7px;text-align:left">
${it.description || ""}
</div>
</a>
</td>
</tr>`);
                    });
                else $tbody.append(`<tr><td colspan="3" style="text-align:center;color:#EEEEEE;font-weight:bold;font-size:22px;">No matching results</td></tr>`);
                $("#resultsTable").show();
                localStorage.setItem("last_search_term", q);
                first = false;
            },
            error: () => {
                $('#loading').hide();
                first = false;
                console.error("Error fetching results");
            }
        });
    }

    $(document).on('click', '.dropdown-content a', function (e) {
        e.preventDefault();
        const text = $(this).children().first().text().trim().toLowerCase();
        const $input = $('#topic');
        if (!$input.val().includes(text))
            $input.val(($input.val() ? $input.val() + ' ' : '') + text + ' ');
        $input.focus();
        lastUpdate = Date.now();
        request();
    });

    $topic.on("keyup", ()=>{
        const now = Date.now();
        if (now - lastUpdate < delay && !first) {
            clearTimeout(pending);
            pending = setTimeout(request, delay);
            return;
        }
        lastUpdate = now;
        request();
    });
}

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