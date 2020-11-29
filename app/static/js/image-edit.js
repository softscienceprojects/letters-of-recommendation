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

const imagesDivs = document.querySelectorAll('.post-image-form')

if (imagesDivs) {
  imagesDivs.forEach(function(n) {
    var img = n.querySelector('img');
    var input = n.querySelector('input');
    img.addEventListener('click', function(e) {
        input.checked = true;
        e.target.parentElement.classList.add('button-shadow-bone');
    })
    // imagsDivs[0].parentElement
    input.addEventListener('change', function(e) {
      console.log(e)

    })
    // if (input.checked === false) {
    //   input.parentElement.classList.remove('button-shadow-bone')
    // }
  })
}
