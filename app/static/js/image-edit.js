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
   