let token = "";
let pingTimer = null;
let first_check = true;

// Read token from cookie
document.cookie.split(";").forEach(cookie => {
    const [name, value] = cookie.trim().split("=");
    if (name === "access_token") {
        token = value;
    }
});

//checkToken(); // refreshes token periodically, if the server has restarted it logs us out
//
//function checkToken() {
//    if(!token)
//        return;
//    $.ajax({
//        url: "http://127.0.0.1:5000/ping",
//        method: "GET",
//        headers: { "Authorization": "Bearer " + token },
//        success: function (response) {
//            if (response && response.token) {
//                token = response.token;
//                const expiresIn = response.expires_in || 3600;
//                document.cookie = "access_token=" + token + "; path=/; max-age=" + expiresIn + ";";
//                clearTimeout(pingTimer);
//                const halfLife = (expiresIn * 1000) / 2;
//                pingTimer = setTimeout(checkToken, halfLife);
//            } else {
//                token = "";
//                document.cookie = "access_token=" + token + "; path=/; max-age=" + expiresIn + ";";
//                location.reload();
//            }
//        },
//        error: function () {
//            token = "";
//            document.cookie = "access_token=" + token + "; path=/; max-age=" + expiresIn + ";";
//            location.reload();
//        }
//    });
//}