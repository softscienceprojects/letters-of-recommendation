init = function() {
    if (document.querySelector('#open-user-menu')) {
        window.app.USER_OPTIONS = 'closed';
        document.querySelector('#open-user-menu').addEventListener('click', function(e) {return openUserMenu(e)} )
    }
}


openUserMenu = function(e) {
    e.preventDefault();
    let userOptionMenu = document.querySelector('#user-options-menu'),
        userMenuButton = document.querySelector('#open-user-menu');
    if (window.app.USER_OPTIONS === "closed") {
        userMenuButton.classList.add("button-shadow-clay")
        userOptionMenu.style.display = "flex";
        window.app.USER_OPTIONS = "open"  
    } else {
        userOptionMenu.style.display = "none";
        userMenuButton.classList.remove("button-shadow-clay")
        window.app.USER_OPTIONS = "closed" 
    }
}


window.onload = init;
document.addEventListener("DOMContentLoaded", init, false);