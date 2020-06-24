//if (window.location.href.indexOf('/posts') > -1) {

const confirmDeleteButton = document.querySelector("#delete-post");

confirmDeleteButton.addEventListener("click", async () => {
  const dialog = new ConfirmDialog({
    confirmButtonText: "Delete",
    cancelButtonText: "Cancel",
    questionText: "Are you sure you would like to delete this post? This action cannot be undone"
  });

  const confirmDelete = await dialog.confirm();
  if (confirmDelete) {
    //let id = window.location.pathname.split('/')[2]
    ///posts/<int:post_id>/delete/
    //"posts/" + pathname[2] +posts/${id}/
    window.app.destroy()
  }
});

