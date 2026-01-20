function handbookGoTo(id) {
    document.getElementById(id).scrollIntoView();
}


handbookBodyElement = document.getElementById("handbookBody");
const bodyIds = Array.from(handbookBodyElement.querySelectorAll('[id]')).map(el => el.id);
let previousActiveId = bodyIds[0];

handbookBodyElement.addEventListener("scroll", (event) => { 
    getActiveMenuItem();
})

function getActiveMenuItem() {
    for (let i=bodyIds.length-1; i>-1; i--){
        const bodyElement = document.getElementById(bodyIds[i])
        if (bodyElement.getBoundingClientRect().top - 10<=0) {
            if (previousActiveId === bodyIds[i]) {break;}
            if (previousActiveId) {
                document.getElementById(previousActiveId + 'Menu').classList.remove('active');
            }
            previousActiveId = bodyIds[i];
            document.getElementById(bodyIds[i] + 'Menu').classList.add('active');
            break;
        }
    }
}


let menuIsVisible = true;
function toggleMenuVisibility() {
    const handbookMenuEl = document.getElementById('handbookMenu');
    const hideMenuBtnEl = document.getElementById('hideMenuBtn');
    if (menuIsVisible) {
        handbookMenuEl.classList.add('hidden');
        hideMenuBtnEl.textContent = '▸';
        menuIsVisible = false;
    }
    else {
        handbookMenuEl.classList.remove('hidden');
        hideMenuBtnEl.textContent = '◂';
        menuIsVisible = true;
    }
}