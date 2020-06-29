class ConfirmDialog {
    // with thanks https://codepen.io/sindre/pen/RwbvObK
  constructor({ questionText, confirmButtonText, cancelButtonText, parent }) {
    this.questionText = questionText || "Are you sure?";
    this.confirmButtonText = confirmButtonText || "Yes";
    this.cancelButtonText = cancelButtonText || "No";
    this.parent = parent || document.body;

    this.dialog = undefined;
    this.confirmButton = undefined;
    this.cancelButton = undefined;

    this._createDialog();
    this._appendDialog();
  }

  confirm() {
    return new Promise((resolve, reject) => {
      const cannotCreateConfirm =
        !this.dialog || !this.confirmButton || !this.cancelButton;
      if (cannotCreateConfirm) {
        reject('Sorry, something went wrong. Please try later.');
        return;
      }
      
      this.dialog.showModal();

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
    this.dialog = document.createElement("dialog");
    // dialog is its own HTML element (API)
    this.dialog.classList.add("confirm-dialog");

    const question = document.createElement("div");
    question.textContent = this.questionText;
    question.classList.add("confirm-dialog-question");
    this.dialog.appendChild(question);

    const buttonGroup = document.createElement("div");
    buttonGroup.classList.add("confirm-dialog-button-group");
    this.dialog.appendChild(buttonGroup);

    this.cancelButton = document.createElement("button");
    this.cancelButton.classList.add(
      "confirm-dialog-button",
      "button-base"
    );
    this.cancelButton.type = "button";
    this.cancelButton.textContent = this.cancelButtonText;
    buttonGroup.appendChild(this.cancelButton);

    this.confirmButton = document.createElement("button");
    this.confirmButton.classList.add(
      "confirm-dialog-button",
      "button-base",
      "button-danger"
    );
    this.confirmButton.type = "button";
    this.confirmButton.textContent = this.confirmButtonText;
    buttonGroup.appendChild(this.confirmButton);
  }

  _appendDialog() {
    this.parent.appendChild(this.dialog);
  }

  _destroy() {
    this.parent.removeChild(this.dialog);
    delete this;
  }
} // end ConfirmDialog



class CommentForm extends HTMLDivElement {
  constructor() {
    super()
  }
}

customElements.define('comment-form', CommentForm, {extends: 'div'})


class Navigation extends HTMLElement {
  constructor() {
    super()
    //let shadow = elementRef.attachShadow({mode: 'open'});
    //let navShadow = navdiv.attachShadow({mode: 'open'});
    const shadow = this.attachShadow({mode: 'open'});
    const info = document.createElement('span');
    const text = this.getAttribute('data-text');
    info.textContent = text;
  }

}

customElements.define('menu-nav', Navigation) //{extends: 'nav'}