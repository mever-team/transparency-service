let token = "";
let pingTimer = null;

// incoming token from registration verification redirect
const params = new URLSearchParams(window.location.search);
const incomingBearer = params.get("token");
const incomingExpiry = params.get("expires_in");
if (incomingBearer) {
    document.cookie = "access_token=" + incomingBearer + "; path=/; max-age=" + (incomingExpiry || 3600) + ";";
    const clean = window.location.origin + window.location.pathname;
    window.history.replaceState({}, document.title, clean);
}

document.cookie.split(";").forEach(cookie => {
    const [name, value] = cookie.trim().split("=");
    if (name === "access_token") token = value;
});

let token_prefix = "Bearer"
function initKeycloak() {
    if (!token && window.Keycloak /*&& window.location.origin.startsWith('https://shell-ui-aicode.ilabhub.atc.gr')*/) {
        console.log(window.location.origin);
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

if (window.Keycloak) initKeycloak();
else window.addEventListener('keycloak-check-done', initKeycloak, { once: true });

function updateUsername() {
//    TODO: THIS SECTION IS DISABLED BECAUSE WE NEED TO PING BASED ON COOKIES BUT FIND A WAY TO RE-ENABLE IT MAYBE
//    OTHERWISE WE GET THE AJAX RESPONSE TO DISABLE THE PING TIMER
//    if (!token) {
//        clearTimeout(pingTimer);
//        $('#new_card').addClass("hidden");
//        $('#login-btn').removeClass("hidden");
//        $('#logout-btn').addClass("hidden");
//        $('#account-btn').addClass("hidden");
//        // $('#user-filter').addClass("hidden");
//        $('#login-name').text("");
//        return;
//    }

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
                $('#new_card').addClass("hidden");
                $('#login-btn').removeClass("hidden");
                $('#logout-btn').addClass("hidden");
                $('#account-btn').addClass("hidden");
                // $('#user-filter').addClass("hidden");
                $('#login-name').text("");
            }
        },
        error: function () {
            clearTimeout(pingTimer);
            document.cookie = "access_token=; path=/; max-age=0;";
            token = "";
            $('#new_card').addClass("hidden");
            $('#login-btn').removeClass("hidden");
            $('#logout-btn').addClass("hidden");
            $('#account-btn').addClass("hidden");
            // $('#user-filter').addClass("hidden");
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
