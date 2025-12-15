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