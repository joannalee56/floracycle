// Disabling form submissions if there are invalid fields

(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    let forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }
  
          form.classList.add('was-validated')
        }, false)
      })
  })()

// if wedding checked
//   document.querySelector('#wedding').onclick
  
//   removeAttribute('checked')



// Update endpoint function - Ajax

// document.querySelector('#wedding').addEventListener('click', evt => {
//   evt.preventDefault();

//   const formInputs = {
//     type: document.querySelector('#type-field').value,
//     amount: document.querySelector('#amount-field').value,
//   };

//   fetch('/new-order', {
//     method: 'POST',
//     body: JSON.stringify(formInputs),
//     headers: {
//       'Content-Type': 'application/json',
//     },
//   })
//     .then(response => response.json())
//     .then(responseJson => {
//       alert(responseJson.status);
//     });
// });