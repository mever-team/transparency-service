let token = "";
let pingTimer = null;

document.cookie.split(";").forEach(cookie => {
    const [name, value] = cookie.trim().split("=");
    if (name === "access_token") {
        token = value;
    }
});

updateUsername();

function updateUsername() {
    if (!token) {
        clearTimeout(pingTimer);
        $('#new_card').hide();
        $('#login-btn').show();
        $('#register-btn').show();
        $('#logout-btn').hide();
        $('#account-btn').hide();
        // $('#user-filter').hide();
        $('#login-name').text("");
        return;
    }

    $.ajax({
        url: "/transparency/ping",
        method: "GET",
        headers: { "Authorization": "Bearer " + token },
        success: function (response) {
            if (response && response.token) {
                token = response.token;
                const expiresIn = response.expires_in || 3600;
                document.cookie = "access_token=" + token + "; path=/; max-age=" + expiresIn + ";";

                $('#new_card').show();
                $('#login-btn').hide();
                $('#register-btn').hide();
                $('#logout-btn').show();
                $('#account-btn').show();
                $('#user-filter').show();
                $('#account-name').text(response.username);

                clearTimeout(pingTimer);

                // Schedule the next ping at half the expiration time
                const halfLife = (expiresIn * 1000) / 2;
                pingTimer = setTimeout(() => {
                    $.ajax({
                        url: "/transparency/ping",
                        method: "GET",
                        headers: { "Authorization": "Bearer " + token },
                        success: function (pingResp) {
                            if (pingResp && pingResp.token) {
                                token = pingResp.token;
                                document.cookie = "access_token=" + token + "; path=/; max-age=" + pingResp.expires_in + ";";
                                updateUsername(); // Refresh UI and reschedule next ping
                            } else {
                                token = "";
                                document.cookie = "access_token=; path=/; max-age=0;";
                                updateUsername();
                            }
                        },
                        error: function () {
                            token = "";
                            document.cookie = "access_token=; path=/; max-age=0;";
                            updateUsername();
                        }
                    });
                }, halfLife);
            } else {
                clearTimeout(pingTimer);
                document.cookie = "access_token=; path=/; max-age=0;";
                token = "";
                $('#new_card').hide();
                $('#login-btn').show();
                $('#register-btn').show();
                $('#logout-btn').hide();
                $('#account-btn').hide();
                // $('#user-filter').hide();
                $('#login-name').text("");
            }
        },
        error: function () {
            clearTimeout(pingTimer);
            document.cookie = "access_token=; path=/; max-age=0;";
            token = "";
            $('#new_card').hide();
            $('#login-btn').show();
            $('#register-btn').show();
            $('#logout-btn').hide();
            $('#account-btn').hide();
            // $('#user-filter').hide();
            $('#login-name').text("");
        }
    });
}

// Ensure timer clears when logging out
$('#logout-btn').on('click', ()=>{
    clearTimeout(pingTimer);
    token = "";
    document.cookie = "access_token=; path=/; max-age=0;";
    updateUsername();
});
