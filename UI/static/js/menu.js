// static/js/script.js

function showVersionControl() {
    document.getElementById('main-menu').style.display = 'none';
    document.getElementById('version-control-menu').style.display = 'block';
    document.getElementById('considerations-menu').style.display = 'none';
}

function showMainMenu() {
    document.getElementById('main-menu').style.display = 'block';
    document.getElementById('version-control-menu').style.display = 'none';
    document.getElementById('considerations-menu').style.display = 'none';
}
