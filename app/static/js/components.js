class ConfirmDialog {
    // with thanks https://codepen.io/sindre/pen/RwbvObK
  constructor({ confirmHeader, questionText, confirmButtonText, cancelButtonText, parent }) {
    this.confirmHeader = confirmHeader || "";
    this.questionText = questionText || "Are you sure?";
    this.confirmButtonText = confirmButtonText || "Yes";
    this.cancelButtonText = cancelButtonText || "No";
    this.parent = parent || document.body;

    this.dialog = undefined;
    this.back = undefined;
    this.confirmButton = undefined;
    this.cancelButton = undefined;

    this._createDialog();
    this._appendDialog();
  }

  confirm() {
    return new Promise((resolve, reject) => {
      const cannotCreateConfirm =
        !this.dialog || !this.confirmButton || !this.cancelButton || !this.back;
      if (cannotCreateConfirm) {
        reject('Sorry, something went wrong. Please try later.');
        return;
      }
      //this.dialog.showModal(); //doesn't work in safari...

      this.confirmButton.addEventListener("click", () => {
        resolve(true);
        this._destroy();
      });

      this.cancelButton.addEventListener("click", () => {
        resolve(false);
        this._destroy();
      });
    });
  }

  _createDialog() {
    this.back = document.createElement("div");
    this.back.classList.add('modal-background');

    this.dialog = document.createElement("div");
    // dialog is its own HTML element (API)
    this.dialog.classList.add("confirm-dialog");
    this.dialog.setAttribute("role", "alertdialog");
    this.dialog.setAttribute('tabindex', '0');

    const question = document.createElement("div");
    if (this.confirmHeader.length) {
        const questionHeader = document.createElement("h1");
        questionHeader.innerText = this.confirmHeader;
        question.append(questionHeader);
    }
    const pQuestion = document.createElement("p");
    pQuestion.textContent = this.questionText;
    question.append(pQuestion);
    
    this.dialog.appendChild(question);

    const buttonGroup = document.createElement("div");
    buttonGroup.classList.add("confirm-dialog-button-group");
    this.dialog.appendChild(buttonGroup);

    this.cancelButton = document.createElement("button");
    this.cancelButton.classList.add(
      "button-base",
      "button-base-rounded",
      "bg-bone"
    );
    this.cancelButton.type = "button";
    this.cancelButton.id = "overlay-cancel";
    this.cancelButton.textContent = this.cancelButtonText;
    buttonGroup.appendChild(this.cancelButton);

    this.confirmButton = document.createElement("button");
    this.confirmButton.id = "overlay-confirm";
    this.confirmButton.classList.add(
      "button-base",
      "button-base-rounded",
      "bg-rust"
    );
    this.confirmButton.type = "button";
    this.confirmButton.textContent = this.confirmButtonText;
    buttonGroup.appendChild(this.confirmButton);
  }

  _appendDialog() {
    // this.parent.aria-hidden="true"
    this.parent.appendChild(this.back);
    this.parent.appendChild(this.dialog);
    this.dialog.focus();
  }

  _destroy() {
    this.parent.removeChild(this.back);
    this.parent.removeChild(this.dialog);
    delete this;
  }
} // end ConfirmDialog


///////////////////////////////////////////////////////////////

// class ConfirmOverlay {
//   constructor({ questionText, confirmButtonText, cancelButtonText, parent }) {
//     this.questionText = questionText || "Are you sure?";
//     this.confirmButtonText = confirmButtonText || "Yes";
//     this.cancelButtonText = cancelButtonText || "No";
//     this.parent = parent || document.body;

//     this.confirmOverlay = undefined;
//     this.confirmButton = undefined;
//     this.cancelButton = undefined;

//     this._createConfirmOverlay();
//     this._appendConfirmOverlay();

//   }

//   _createConfirmOverlay() {

//     this.confirmOverlay = document.createElement('div')
//   }
  

// }


class ImageUploader { 
  constructor({parent}) {
    this.upload_div = undefined
    this.parent = parent || document.body

    
    this._create_uploader_form()
    this._append()
    document.querySelector('button#image-upload').disabled = true;
  }

  _create_uploader_form() {
    this.upload_div = document.createElement('dialog')
    this.upload_div.classList.add('image-upload')
    
    const form = document.createElement('form')
    form.enctype = "multipart/form-data"
    form.action = ""
    form.method = "post"

    const hidden = document.createElement('input')
    hidden.type = "hidden"
    hidden.name = "csrf_token"
    hidden.value = "???"

    const input = document.createElement('input')
    input.type = "file"
    input.name = "file"

    const upload = document.createElement('input')
    upload.type = "submit"
    upload.value = "upload"
    upload.innerText = "Upload image"
    // upload.disabled = true;  // keep disabled until input.files.length > 0; (needs eventlistener)

    form.appendChild(hidden)
    form.appendChild(input)
    form.appendChild(upload)
    this.upload_div.appendChild(form)
  }

  _append() {
    this.parent.appendChild(this.upload_div)
  }
}

//////////////////////////////////////////////////////////////////

// class ImageDialog {
//   constructor({ parent }) {
//     this.parent = parent || document.body;

//     this.dialog = undefined;
//     this.confirmButton = undefined;
//     this.cancelButton = undefined;

//     this._createDialog();
//     this._appendDialog();
//   }

//   confirm() {
//     return new Promise((resolve, reject) => {
//       const cannotCreateConfirm =
//         !this.dialog || !this.confirmButton || !this.cancelButton;
//       if (cannotCreateConfirm) {
//         reject('Sorry, something went wrong. Please try later.');
//         return;
//       }

//       this.dialog.showModal();

//       this.confirmButton.addEventListener("click", () => {
//         resolve(true);
//         this._destroy();
//       });

//       this.cancelButton.addEventListener("click", () => {
//         resolve(false);
//         this._destroy();
//       });
//     });
//   }

//   _createDialog() {
//     this.dialog = document.createElement("dialog");
//     // dialog is its own HTML element (API)
//     this.dialog.classList.add("confirm-dialog");

//     const question = document.createElement("div");
//     question.textContent = this.questionText;
//     question.classList.add("confirm-dialog-question");
//     this.dialog.appendChild(question);

//     const buttonGroup = document.createElement("div");
//     buttonGroup.classList.add("confirm-dialog-button-group");
//     this.dialog.appendChild(buttonGroup);

//     this.cancelButton = document.createElement("button");
//     this.cancelButton.classList.add(
//       "confirm-dialog-button",
//       "button-base"
//     );
//     this.cancelButton.type = "button";
//     this.cancelButton.textContent = this.cancelButtonText;
//     buttonGroup.appendChild(this.cancelButton);

//     this.confirmButton = document.createElement("button");
//     this.confirmButton.classList.add(
//       "confirm-dialog-button",
//       "button-base",
//       "button-danger"
//     );
//     this.confirmButton.type = "button";
//     this.confirmButton.textContent = this.confirmButtonText;
//     buttonGroup.appendChild(this.confirmButton);
//   }

//   _appendDialog() {
//     this.parent.appendChild(this.dialog);
//   }

//   _destroy() {
//     this.parent.removeChild(this.dialog);
//     delete this;
//   }
// } // end ImageDialog