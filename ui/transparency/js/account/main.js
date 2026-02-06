$(function () {
    $('#logout-btn').click(() => { token = ""; document.cookie = "access_token=; path=/; max-age=0;"; window.location.href = 'index.html'; });
    $('#loading').show();
    $.ajax({
        url: "/transparency/users",
        contentType: "application/json",
        dataType: "json",
        headers: {"Authorization": "Bearer " + token},
        success: function (response) {
            const $pending = $("#pending-users").empty();
            if (response.pending.length === 0) $pending.hide();
            else response.pending.forEach(u => {
                $pending.append(`
                    <div class="user">
                        <span style="username">${u.username}</span> - ${u.email || "no contact info"}
                        <span class="delete-btn error button" data-username="${u.username}"><i class="fa-solid fa-cancel"></i>&nbsp;Reject</span>
                        <span class="pending-btn warning button" data-username="${u.username}"><i class="fa-solid fa-key"></i>&nbsp;Accept</span>
                    </div>
                `);
            });
            const $registered = $("#registered-users").empty();
            if (response.users.length === 0) $registered.hide();
            else response.users.forEach(u => { $registered.append(`
                <div class="user">
                    <span class="username">${u.username}</span> - ${u.email||"no contact info"}
                    <span class="delete-btn error button" data-username="${u.username}"><i class="fa-solid fa-cancel"></i>&nbsp;Delete</span>
                    <span class="registered-label">Registered</span>
                </div>
            `);});
            $(".is-admin").show();
            $('#loading').hide();
        },
        error: {}
    });
    $(document).on('click', '.pending-btn', function () {
        const username = $(this).data('username');
        $.ajax({
            url: `/transparency/users/${username}/accept`,
            method: "POST",
            headers: { "Authorization": "Bearer " + token },
            success: function () {
                location.reload(); // simplest + safest refresh
            },
            error: function (xhr) {
                alert(xhr.responseJSON?.error || "Failed to accept user");
            }
        });
    });
    $(document).on('click', '.delete-btn', function () {
        const username = $(this).data('username');
        if(username === loggedUser) {
            if (!confirm(`Delete your account? This will remove all your data, including created model cards, and cannot be undone.`)) return;
        }
        else if(!confirm(`Remove user "${username}"? This will remove all their data, including model cards, and cannot be undone.`)) return;
        $.ajax({
            url: `/transparency/users/${username}`,
            method: "DELETE",
            headers: { "Authorization": "Bearer " + token },
            success: function () {
            if(username === loggedUser) {
                token = "";
                document.cookie = "access_token=; path=/; max-age=0;";
                window.location.href = "index.html";
            }
            else  location.reload();
        },
            error: xhr => alert(xhr.responseJSON?.error || "Failed to delete user")
        });
    });
});