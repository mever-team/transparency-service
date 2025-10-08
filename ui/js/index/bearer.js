let token = "";
document.cookie.split(";").forEach(cookie => {
    const [name, value] = cookie.trim().split("=");
    if (name === "access_token") {
        token = value;
    }
});

updateUsername();

function updateUsername() {
    document.cookie = "access_token=" + token + "; path=/; max-age=3600;";
    if(token) {
        $('#new_card').show();
        $('#login-btn').hide();
        $('#logout-btn').show();
        //$('#login-name').text("Welcome!");
    }
    else {
        $('#new_card').hide();
        $('#login-btn').show();
        $('#logout-btn').hide();
        $('#login-name').text("");
    }
}