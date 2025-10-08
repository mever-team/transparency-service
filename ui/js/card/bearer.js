let token = "";
document.cookie.split(";").forEach(cookie => {
    const [name, value] = cookie.trim().split("=");
    if (name === "access_token") {
        token = value;
    }
});
