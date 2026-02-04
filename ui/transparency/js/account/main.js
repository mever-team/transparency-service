$(document).ready(function () {
    $.ajax({
        url: "/transparency/users",
        contentType: "application/json",
        dataType: "json",
        headers: {"Authorization": "Bearer " + token},
        success: function (response) {
            const $pending = $("#pending-users").empty();
            if (response.pending.length === 0) $pending.hide();
            else response.pending.forEach(u => {$pending.append(`
                <div style="border:1px solid #434343;padding:15px;color:#7C7C7C; margin-bottom:10px">
                <span style="font-size:16px;color:#79CFDC">${u.username}</span> - ${u.email||"no contact info"}
                <span style="float: right;color:#64DB96">pending</span></div>
            `);});
            const $registered = $("#registered-users").empty();
            if (response.users.length === 0) $registered.hide();
            else response.users.forEach(u => { $registered.append(`
                <div style="border:1px solid #434343;padding:15px;color:#7C7C7C; margin-bottom:10px">
                <span style="font-size:16px;color:#79CFDC">${u.username}</span> - ${u.email||"no contact info"}
                <span style="float: right;color:#64DB96">registered</span></div>
            `);});
            $(".is-admin").show();
        },
        error: {}
    });
});