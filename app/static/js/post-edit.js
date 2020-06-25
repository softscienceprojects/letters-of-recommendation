
const tagsInput = document.querySelector("input#tags");
const tagsDiv = document.querySelector("div#tags")
let word = ''
let words = []

tagsInput.addEventListener('input', function(e) { 
    if (e.data === ',') {
        words.push(word)
        let pTag = document.createElement('button')
        pTag.classList.add('tag-list-highlight')
        pTag.innerText = word
        pTag.addEventListener('click', tagButtonClicked)
        tagsDiv.appendChild(pTag)
        word = ''
    } else if (e.data===null) {
        if (!words.includes(tagsInput.value)) {
            words.pop()
        }
    } else {
        word += e.data
    }
})

tagButtonClicked = function(e) {
    e.preventDefault();
    e.target.removeEventListener('click', tagButtonClicked)
    tagsDiv.removeChild(this)
}

// .form-control:valid {
//     background-color: #00FF7F;
//   }