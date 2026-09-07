let token = "";
let pingTimer = null;
let first_check = true;
var loggedUser = "";
var loggedUserNotifications = "";
var loggedUserIsAdmin = false;

// incoming token from registration verification redirect
const params = new URLSearchParams(window.location.search);
const incomingBearer = params.get("token");
const incomingExpiry = params.get("expires_in");
if (incomingBearer) {
    document.cookie = "access_token=" + incomingBearer + "; path=/; max-age=" + (incomingExpiry || 3600) + ";";
    const clean = window.location.origin + window.location.pathname;
    window.history.replaceState({}, document.title, clean);
}

// this needs to be called AFTER the above segments so that we can account for the incoming bearer
document.cookie.split(";").forEach(cookie => {
    const [name, value] = cookie.trim().split("=");
    if (name === "access_token") token = value;
});

let token_prefix = "Bearer"
function initKeycloak() {
    if (!token && window.Keycloak && window.location.origin==='https://proxy-gateway-aicode.ilabhub.atc.gr') {
        const keycloak = new window.Keycloak({
            url: "https://faithkc.ilabhub.atc.gr",
            realm: "shell-app",
            clientId: "shell-ui-proxy"
        });
        const keycloak_auth = async () => {
            try {
                const authenticated = await keycloak.init({
                    onLoad: "check-sso",
                    pkceMethod: "S256",
                    checkLoginIframe: false,
                });
                if (authenticated) {
                    token_prefix = "ThirdPartyBearer";
                    token = keycloak.token;
                }
            } catch (e) {
                console.log("Keycloak init skipped:", e);
            }
            updateUsername();
        }
        keycloak_auth();
    } else updateUsername();
}

if (window.Keycloak) initKeycloak(); // calls updateUsername
else window.addEventListener('keycloak-check-done', initKeycloak, { once: true });

function updateUsername() {
    $.ajax({
        url: "/transparency/ping",
        method: "GET",
        headers: { "Authorization": token_prefix+" " + token },
        success: function (response) {
            if (response && response.token) {
                token = response.token;
                const expiresIn = response.expires_in || 3600;
                document.cookie = "access_token=" + token + "; path=/; max-age=" + expiresIn + ";";
                $('#new_card').removeClass("hidden");
                $('#login-btn').addClass("hidden");
                $('#logout-btn').removeClass("hidden");
                $('#account-btn').removeClass("hidden");
                $('#user-filter').removeClass("hidden");
                $('#account-name').text(response.username+(response.notifications||""));
                
                loggedUser = response.username;
                loggedUserIsAdmin = response.admin;
                loggedUserNotifications = response.notifications;
                $('#account-name').text(loggedUser+(loggedUserNotifications||""));
                
                clearTimeout(pingTimer);
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

                $('#new_card').addClass("hidden");
                $('#login-btn').removeClass("hidden");
                $('#logout-btn').addClass("hidden");
                $('#account-btn').addClass("hidden");
                $('#login-name').text("");
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

            $('#new_card').addClass("hidden");
            $('#login-btn').removeClass("hidden");
            $('#logout-btn').addClass("hidden");
            $('#account-btn').addClass("hidden");
            $('#login-name').text("");
        }
    });
}

$('#logout-btn').on('click', ()=>{
    clearTimeout(pingTimer);
    token = "";
    document.cookie = "access_token=; path=/; max-age=0;";
    updateUsername();
});