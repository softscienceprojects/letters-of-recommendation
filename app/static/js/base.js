BASE_URL = window.location.host + "/";
USER_DEVICE_MOBILE = /Mobile|Touch/i.test(navigator.userAgent);

window.app = {
    destroy: function(path) {
        console.log(path)
        return fetch(path, {method: "POST"})
        .then(response=>response.json())
        .then(response=>window.location.replace(response.next))
        .catch(error=>console.error(error))
    }
}

//const navdiv = document.querySelector('#navigation-menu')
let menuButton = document.querySelector('#menu-button');
let nav = document.querySelector('nav');

closeNav = function() {
    menuButton.innerHTML = USER_DEVICE_MOBILE ? 'MENU' : '<i class="material-icons">fullscreen</i>';
    menuButton.classList.add('menu-button-open')
    menuButton.classList.remove('menu-button-close')
    nav.classList.remove('display-show');
    nav.classList.add('display-hide');
    sessionStorage.setItem('navMenu', 'closed')
}

openNav = function() {
    menuButton.innerHTML = USER_DEVICE_MOBILE ? 'CLOSE MENU' : '<i class="material-icons">fullscreen_exit</i>';
    menuButton.classList.add('menu-button-close')
    menuButton.classList.remove('menu-button-open')
    nav.classList.remove('display-hide');
    nav.classList.add('display-show')
    sessionStorage.setItem('navMenu', 'open')
}

menuButton.addEventListener('click', function(e) {
    if (sessionStorage.getItem('navMenu') === 'open') {
        nav.style.transition = '0.5s';
        closeNav()
    } else {
        nav.style.transition = '0.5s';
        openNav()
    }
})


const imageUploaderButton = document.querySelector("#image-upload")

if (imageUploaderButton) {
    imageUploaderButton.addEventListener("click", async(e) => {
        e.preventDefault()
        const imageUpload = new ImageUploader({parent: document.querySelector('.post-content')})
    })
}

document.body.onload = function() {
    if( !USER_DEVICE_MOBILE ) {
        if (!sessionStorage.getItem('navMenu') || sessionStorage.getItem('navMenu') === 'closed') {
            closeNav()
        } else {
            openNav()
        }
    } else {
        closeNav()
    }   
}