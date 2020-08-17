//CONSTANTS
const tagsInput = document.querySelector("input#tags");
const tagsDiv = document.querySelector("div#tags")
let word = ''
let words = []
var lastFocus;

onInit = function() {
    if (tagsInput.value != "") {
        words = tagsInput.value.split(',')
        words.forEach(word => createButton(word))
    }
    tagsInput.value = ''
}

resetWord = function() {
    word = ''
    tagsInput.value = ''
    //tagsInput.value = words.join(',')
}

tagsInput.addEventListener('input', function(e) {
    if (e.data === ',' && word.length > 1) {
        words.push(word.toLowerCase().trim())
        createButton(word.toLowerCase().trim())
        resetWord()
    } else if (e.data === null || e.data === undefined) {
        word = word.substring(0, word.length-1)
    } else {
        word += e.data
    }
})

createButton = function(word) {
    let tagButton = document.createElement('button')
    tagButton.classList.add('tag-list-highlight')
    tagButton.id = `${word}-`
    tagButton.innerText = word
    tagButton.addEventListener('click', tagButtonClicked)
    tagsDiv.appendChild(tagButton)
    resetWord()
}

tagButtonClicked = function(e) {
    e.preventDefault();
    word = this.innerText;
    e.target.removeEventListener('click', tagButtonClicked)
    tagsDiv.removeChild(this)
    if (words.indexOf(word) > -1) {
        let ind = words.indexOf(word)
        words.splice(ind, 1);
    }
    resetWord()
}

document.querySelector('form.edit-post').addEventListener('submit', function(e) {
    setTimeout(e.preventDefault, 500)
    tagsInput.value = words.join(',')
})



const confirmDeleteButton = document.querySelector("#delete-post");

if (confirmDeleteButton) {
    confirmDeleteButton.addEventListener("click", async () => {
        const dialog = new ConfirmDialog({
          confirmHeader: "Delete this post",
          confirmButtonText: "Delete",
          cancelButtonText: "Cancel",
          questionText: "Are you sure you would like to delete this post? This action cannot be undone"
        });

        lastFocus = confirmDeleteButton;
  
        const confirmDelete = await dialog.confirm();
        if (confirmDelete) {
          let id = window.location.pathname.split('/')[2]
          window.app.destroy(`/posts/${id}/edit/delete/`)
      } else {
          lastFocus.focus();
      }
  });

}
    




document.addEventListener('DOMContentLoaded', function() {
    onInit()
})