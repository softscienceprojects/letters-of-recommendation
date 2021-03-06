window.initImageEditOptions = function() {
  // D E S T O Y
  const confirmDeleteButton = document.querySelector("#delete-image");

  if (confirmDeleteButton) {
      confirmDeleteButton.addEventListener("click", async () => {
          const dialog = new ConfirmDialog({
            confirmButtonText: "Delete",
            cancelButtonText: "Cancel",
            questionText: "Are you sure you would like to delete this image? This action cannot be undone"
          });
        
          const confirmDelete = await dialog.confirm();
          if (confirmDelete) {
            let asset_id = window.location.pathname.split('/')[2]
            window.app.destroy(`/images/${asset_id}/delete/`)
        }

    });
  };
  

  // database call to remove hero from a post

  const removeHeroButton = document.querySelector('#remove-hero')

  if (removeHeroButton) {
      removeHeroButton.addEventListener('click', async () => {
        let id = window.location.pathname.split('/')[2]
        // console.log(id)
        window.app.destroy(`/posts/${id}/remove-hero`)
        }
      )
  }


  // Choose hero by clicking on image

  const imagesDivsMulti = document.querySelectorAll('.image-card')
  const imagesDivsRadio = document.querySelectorAll('.post-image-form') 


  if (imagesDivsMulti.length || imagesDivsRadio.length) {
    imagesDivs = imagesDivsMulti.length ? imagesDivsMulti : imagesDivsRadio
    imagesDivs.forEach(function(n) {
      var img = n.querySelector('img');
      var input = n.querySelector('input');

      img.addEventListener('click', function(e) {
          if (!input.checked) {
            selectImage(input, img, true)
          } else {
            selectImage(input, img, false)
          }
      });
      
        input.addEventListener('change', function(e) {
          if (!input.checked) {
            selectImage(input, img, false)
            } else {
              selectImage(input, img, true)
            }
        })
      

      if (input.checked) {
        img.classList.add('button-shadow-bone');
      }

    })
  }

  function selectImage(input_selected, image, is_checked) {
    if (input_selected['type'] !== 'radio') {
      if (is_checked) {
        input_selected.checked = true; 
        image.classList.add('button-shadow-bone');
      } else {
        input_selected.checked = false;
        image.classList.remove('button-shadow-bone');
      }
    }

    if (input_selected['type'] === 'radio') {
      input_selected.checked = true;
      image.classList.add('button-shadow-bone');
      // input_selected.parentElement.querySelector('img').classList.add('button-shadow-bone');
      let radio_buttons = document.querySelectorAll('input[name="selectHeroList"]');
          for (let rb of radio_buttons) {
              if (!rb.checked ) {
                rb.parentElement.querySelector('img').classList.remove('button-shadow-bone');
              }
          }
    }
  }
} 
