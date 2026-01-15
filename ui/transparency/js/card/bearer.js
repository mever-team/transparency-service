let token = "";
let pingTimer = null;
let first_check = true;

document.cookie.split(";").forEach(cookie => {
    const [name, value] = cookie.trim().split("=");
    if (name === "access_token")
        token = value;
});