//CONSTANTS
const tagsInput = document.querySelector("input#tags");
const tagsDiv = document.querySelector("div#tags")
let word = ''
let words = []

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

document.addEventListener('DOMContentLoaded', function() {
    onInit()
})
