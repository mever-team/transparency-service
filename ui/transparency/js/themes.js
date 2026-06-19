function setDarkTheme(enabled) {
    document.body.classList.toggle('dark-theme', enabled);
    if(enabled){
        $('.footer_section_logo').attr('src', "img/logo.png");
        $('.footer_section_eu').attr('src', "img/logo_FoundedbyEU.png");
    }
}
isDark = localStorage.getItem("isDark") === "true";
setDarkTheme(isDark);