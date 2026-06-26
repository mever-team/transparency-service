themes = [
    "light-theme",
    "dark-theme",
    "ocean-theme",
];

function setTheme(theme) {

    document.body.classList.remove(...themes);
    if (theme && themes.includes(theme)) {
        document.body.classList.add(theme);
    }

    switch(theme) {
        case "dark-theme":
            $('.footer_section_logo').attr('src', 'img/logo_dark.png');
            $('.footer_section_eu').attr('src', 'img/logo_FoundedbyEU_dark.png');
            break;
        default:
            $('.footer_section_logo').attr('src', 'img/logo.png');
            $('.footer_section_eu').attr('src', 'img/logo_FoundedbyEU.png');
    }

    localStorage.setItem("theme", theme);
}

theme = localStorage.getItem("theme") || "light-theme";
setTheme(theme);

