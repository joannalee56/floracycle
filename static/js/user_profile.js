
const deleteButton = document.querySelector('#delete');

deleteButton.addEventListener('click', (evt) => {
  const message = "Are you sure you want to delete this classified? This action is not reversible.";
  if (confirm(message) == true) {
    pass
  } else {
    evt.preventDefault();
  }
});
