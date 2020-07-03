BASE_URL = window.location.host + "/";

window.app = {
    destroy: function() {
        return fetch("delete/", {method: "POST"})
        .then(response=>response.json())
        .then(response=>window.location.replace(response.next))
        .catch(error=>console.error(error))
    }
}

//const navdiv = document.querySelector('#navigation-menu')
let menuButton = document.querySelector('#menu-button');
let nav = document.querySelector('nav');

closeNav = function() {
    nav.classList.add('display-hide');
    nav.classList.remove('display-show');
    sessionStorage.setItem('navMenu', 'closed')
}

openNav = function() {
    nav.classList.remove('display-hide');
    nav.classList.add('display-show')
    sessionStorage.setItem('navMenu', 'open')
}

menuButton.addEventListener('click', function(e) {
    if (sessionStorage.getItem('navMenu') === 'open') {
        closeNav()
    } else {
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
    if (!sessionStorage.getItem('navMenu') || sessionStorage.getItem('navMenu') === 'open') {
        openNav()
    } else {
        closeNav()
    }
}