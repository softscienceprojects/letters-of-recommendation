BASE_URL = window.location.host + "/";
USER_DEVICE_MOBILE = /Mobile|Touch/i.test(navigator.userAgent) || window.innerWidth<900;

window.app = {
    destroy: function(path) {
        //console.log(path)
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
    nav.classList.remove('display-show');
    nav.classList.add('display-hide');
    sessionStorage.setItem('navMenu', 'closed')
}

openNav = function() {
    menuButton.innerHTML = USER_DEVICE_MOBILE ? 'CLOSE MENU' : '<i class="material-icons">fullscreen_exit</i>';
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


function init() {
    // thx https://stackoverflow.com/questions/1235985/attach-a-body-onload-event-with-js
    // quit if this function has already been called
    if (arguments.callee.done) return;
  
    // flag this function so we don't do the same thing twice
    arguments.callee.done = true;
  
    // kill the timer
    if (_timer) clearInterval(_timer);
  
    // do stuff
    return true;
  };
  
  /* for Mozilla/Opera9 */
  if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", init, false);
  }

  
  /* for Safari */
  if (/WebKit/i.test(navigator.userAgent)) { // sniff
    var _timer = setInterval(function() {
      if (/loaded|complete/.test(document.readyState)) {
        init(); // call the onload handler
      }
    }, 10);
  }
  
  /* for other browsers */
  window.onload = init;