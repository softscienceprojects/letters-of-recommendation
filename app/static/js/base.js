BASE_URL = window.location.host + "/";
USER_DEVICE_MOBILE = /Mobile|Touch/i.test(navigator.userAgent) || window.innerWidth<900;

// WINDOW
window.app = {
    destroy: function(path) {
        // console.log(path)
        return fetch(path, {method: "POST"})
        .then(response=>response.json())
        // .then(reponse=>console.log(response))
        .then(response=>window.location.replace(response.next))
        .catch(error=>console.error(error))
    }
}

window.addEventListener("resize", function() {
    USER_DEVICE_MOBILE = /Mobile|Touch/i.test(navigator.userAgent) || window.innerWidth<900;
    if (window.innerWidth < 900) {
        closeNav()
    } else {
        if (sessionStorage.getItem('navMenu') === 'closed') {
            closeNav()
        } else {
            openNav()
        }
    }
})


//const navdiv = document.querySelector('#navigation-menu')
let menuButton = document.querySelector('#menu-button');
let nav = document.querySelector('nav');



closeNav = function() {
    nav.classList.remove('display-show');
    nav.style.transition = '0.5s';
    nav.classList.add('display-hide');
    sessionStorage.setItem('navMenu', 'closed')
}

openNav = function() {
    nav.classList.remove('display-hide');
    nav.style.transition = '0.5s';
    nav.classList.add('display-show');
    sessionStorage.setItem('navMenu', 'open')
}

menuButton.addEventListener('click', function(e) {
    if (sessionStorage.getItem('navMenu') === 'open') {
        // nav.style.transition = '0.5s';
        closeNav()
    } else {
        // nav.style.transition = '0.5s';
        openNav()
    }
})

// const fileUpload = document.querySelector(".form-file-upload")

// if (fileUpload) {
//     let filesSelected = document.querySelector('input[type="file"]')
//     filesSelected.addEventListener("change", function(e) {
//         let filenames = []
//         for (let i=0; i < e.target.files.length; i++) {
//             filenames.push(e.target.files.item(i).name)
//             // e.target.files.item(i).size
//         }
//         let filenamesDisplay = document.querySelector("#file-uploaded")
//         filenamesDisplay.innerText = filenames.join(", ");
//     })
// }

  // on upload images - show images being uploaded
  const uploadedFile = document.querySelector('input[id=images]')
  
  if (uploadedFile) {
    const showImages = document.querySelector('#uploaded-images');
    
    uploadedFile.addEventListener('change', function(event) {
      showImages.replaceChildren()
      for (let file in event.target.files) {
        if (file < event.target.files['length']) {
          let img = document.createElement('img')
          img.src = URL.createObjectURL(event.target.files[file]);
          showImages.appendChild(img)
        }
      }
    })
  }







////// Init stuff out of the way

bodyOnload = function() {
    console.log('(╯°□°）╯︵ ┻━┻')
    closeNav()
    // if( USER_DEVICE_MOBILE ) {
        // menuButton.innerHTML = "MENU";
    // }
    if (window.initImageEditOptions) {
        // not really a sustainable solution...
        window.initImageEditOptions()
    }
    
}


function init() {
    // console.log(arguments)
    // thx https://stackoverflow.com/questions/1235985/attach-a-body-onload-event-with-js
    // quit if this function has already been called
    if (arguments.callee.done) return;
  
    // flag this function so we don't do the same thing twice
    arguments.callee.done = true;
  
    // kill the timer
    if (_timer) clearInterval(_timer);

    // do stuff
    return bodyOnload();
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