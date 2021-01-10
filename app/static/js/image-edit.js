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

  }

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

  const imagesDivsRadio = document.querySelectorAll('.post-image-form') 
  const imagesDivsMulti = document.querySelectorAll('.image-card')

  if (imagesDivsRadio.length || imagesDivsMulti.length) {
    imagesDivs = imagesDivsRadio.length ? imagesDivsRadio : imagesDivsMulti
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

  function selectImage(checkbox, image, is_checked) {
    if (is_checked) {
      checkbox.checked = true; 
      image.classList.add('button-shadow-bone');
    } else {
      checkbox.checked = false;
      image.classList.remove('button-shadow-bone');
    }
  }
} 
