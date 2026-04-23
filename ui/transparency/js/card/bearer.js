let token = "";
let pingTimer = null;
let first_check = true;
var loggedUser = "";
var loggedUserNotifications = "";
var loggedUserIsAdmin = false;

document.cookie.split(";").forEach(cookie => {
    const [name, value] = cookie.trim().split("=");
    if(name === "access_token")
        token = value;
});

updateUsername();

function updateUsername() {
//    TODO: THIS SECTION IS DISABLED BECAUSE WE NEED TO PING BASED ON COOKIES BUT FIND A WAY TO RE-ENABLE IT MAYBE
//    OTHERWISE WE GET THE AJAX RESPONSE TO DISABLE THE PING TIMER
//    if (!token) {
//        clearTimeout(pingTimer);
//        return;
//    }
    $.ajax({
        url: "/transparency/ping",
        method: "GET",
        headers: { "Authorization": "Bearer " + token },
        success: function (response) {
            if (response && response.token) {
                token = response.token;
                const expiresIn = response.expires_in || 3600;
                document.cookie = "access_token=" + token + "; path=/; max-age=" + expiresIn + ";";
                loggedUser = response.username;
                loggedUserIsAdmin = response.admin;
                loggedUserNotifications = response.notifications;
                $('#account-name').text(loggedUser+(loggedUserNotifications||""));
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
                                loggedUser = pingResp.username;
                                loggedUserIsAdmin = response.admin;
                                loggedUserNotifications = pingResp.loggedUserNotifications;
                                document.cookie = "access_token=" + token + "; path=/; max-age=" + pingResp.expires_in + ";";
                                updateUsername(); // Refresh UI and reschedule next ping
                                $('#account-name').text(loggedUser+(loggedUserNotifications||""));
                            } else {
                                token = "";
                                loggedUser = "";
                                loggedUserNotifications = "";
                                document.cookie = "access_token=; path=/; max-age=0;";
                                updateUsername();
                                $('#account-name').text(loggedUser);
                            }
                        },
                        error: function () {
                            token = "";
                            loggedUser = "";
                            loggedUserIsAdmin = false;
                            loggedUserNotifications = "";
                            document.cookie = "access_token=; path=/; max-age=0;";
                            updateUsername();
                            $('#account-name').text(loggedUser);
                        }
                    });
                }, halfLife);
            } else {
                clearTimeout(pingTimer);
                token = "";
                loggedUser = "";
                loggedUserIsAdmin = false;
                loggedUserNotifications = "";
                document.cookie = "access_token=; path=/; max-age=0;";
                $('#account-name').text(loggedUser);
            }
        },
        error: function () {
            clearTimeout(pingTimer);
            document.cookie = "access_token=; path=/; max-age=0;";
            token = "";
            loggedUser = "";
            loggedUserIsAdmin = false;
            loggedUserNotifications = "";
            $('#account-name').text(loggedUser);
        }
    });
}