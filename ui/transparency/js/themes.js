themes = [
    "light-theme",
    "dark-theme",
    "ocean-theme",
];

function setTheme(theme) {

    let themeToSet = theme;
    if (theme === "system-theme") {
        themeToSet = window.matchMedia("(prefers-color-scheme: dark)").matches
            ? "dark-theme"
            : "light-theme";
    }
    
    document.body.classList.remove(...themes);
    if (themeToSet && themes.includes(themeToSet)) {
        document.body.classList.add(themeToSet);
    }

    switch(themeToSet) {
        case "dark-theme":
            $('.footer_section_logo').attr('src', 'img/logo.png');
            $('.footer_section_eu').attr('src', 'img/logo_FoundedbyEU.png');
            break;
        case "ocean-theme":
            $('.footer_section_logo').attr('src', 'img/logo.png');
            $('.footer_section_eu').attr('src', 'img/logo_FoundedbyEU.png');
            break;
        default:
            $('.footer_section_logo').attr('src', 'img/logo_og.png');
            $('.footer_section_eu').attr('src', 'img/logo_FoundedbyEU_black.png');
            // theme = 'light-theme';
    }

    localStorage.setItem("theme", theme);
}

theme = localStorage.getItem("theme") || "system-theme";
if (isInIframe()) {
    theme = "light-theme";
}
setTheme(theme);

