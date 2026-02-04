function handbookGoTo(id) {
    document.getElementById(id).scrollIntoView();
}


handbookBodyElement = document.getElementById("handbookBody");
const bodyIds = Array.from(handbookBodyElement.querySelectorAll('[id]')).map(el => el.id);
let previousActiveId = bodyIds[0];

document.addEventListener("scroll", (event) => { getActiveMenuItem(); });

function getActiveMenuItem() {
    for (let i=bodyIds.length-1; i>-1; i--){
        const bodyElement = document.getElementById(bodyIds[i]);
        console.log(bodyElement.getBoundingClientRect().top);
        if (bodyElement.getBoundingClientRect().top - 10<=0) {
            if (previousActiveId === bodyIds[i]) {return;}
            document.getElementById(previousActiveId + 'Menu').classList.remove('active');
            previousActiveId = bodyIds[i];
            document.getElementById(bodyIds[i] + 'Menu').classList.add('active');
            return;
        }
    }
    // If all getBoundingClientRect().top >0
    document.getElementById(previousActiveId + 'Menu').classList.remove('active');
    previousActiveId = bodyIds[0];
    document.getElementById(bodyIds[0] + 'Menu').classList.add('active');
}


let menuIsVisible = true;
function toggleMenuVisibility() {
    const handbookMenuEl = document.getElementById('handbookMenu');
    const hideMenuBtnEl = document.getElementById('hideMenuBtn');
    if(menuIsVisible) handbookMenuEl.classList.add('hidden');
    else handbookMenuEl.classList.remove('hidden');
    hideMenuBtnEl.textContent = menuIsVisible?'▸':'◂';
    menuIsVisible = !menuIsVisible;
}