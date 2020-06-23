//if (window.location.href.indexOf('/posts') > -1) {

const confirmDeleteButton = document.querySelector("#delete-post");

confirmDeleteButton.addEventListener("click", async () => {
  const dialog = new ConfirmDialog({
    trueButtonText: "Delete",
    falseButtonText: "Cancel",
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

class ConfirmDialog {
    // with thanks https://codepen.io/sindre/pen/RwbvObK
  constructor({ questionText, trueButtonText, falseButtonText, parent }) {
    this.questionText = questionText || "Are you sure?";
    this.trueButtonText = trueButtonText || "Yes";
    this.falseButtonText = falseButtonText || "No";
    this.parent = parent || document.body;

    this.dialog = undefined;
    this.trueButton = undefined;
    this.falseButton = undefined;

    this._createDialog();
    this._appendDialog();
  }

  confirm() {
    return new Promise((resolve, reject) => {
      const somethingWentWrongUponCreation =
        !this.dialog || !this.trueButton || !this.falseButton;
      if (somethingWentWrongUponCreation) {
        reject('Sorry, something went wrong. Please try later.');
        return;
      }
      
      this.dialog.showModal();

      this.trueButton.addEventListener("click", () => {
        resolve(true);
        this._destroy();
      });

      this.falseButton.addEventListener("click", () => {
        resolve(false);
        this._destroy();
      });
    });
  }

  _createDialog() {
    this.dialog = document.createElement("dialog");
    this.dialog.classList.add("confirm-dialog");

    const question = document.createElement("div");
    question.textContent = this.questionText;
    question.classList.add("confirm-dialog-question");
    this.dialog.appendChild(question);

    const buttonGroup = document.createElement("div");
    buttonGroup.classList.add("confirm-dialog-button-group");
    this.dialog.appendChild(buttonGroup);

    this.falseButton = document.createElement("button");
    this.falseButton.classList.add(
      "confirm-dialog-button",
      "confirm-dialog-button--false"
    );
    this.falseButton.type = "button";
    this.falseButton.textContent = this.falseButtonText;
    buttonGroup.appendChild(this.falseButton);

    this.trueButton = document.createElement("button");
    this.trueButton.classList.add(
      "confirm-dialog-button",
      "confirm-dialog-button--true"
    );
    this.trueButton.type = "button";
    this.trueButton.textContent = this.trueButtonText;
    buttonGroup.appendChild(this.trueButton);
  }

  _appendDialog() {
    this.parent.appendChild(this.dialog);
  }

  _destroy() {
    this.parent.removeChild(this.dialog);
    delete this;
  }
}