
// document.querySelector('.profile-button').onclick = function() {
//     if (document.querySelector('#to-disable').disabled == true) {
//         document.querySelector('#to-disable').disabled = false;
//         document.querySelector('.profile-button').innerText = "Save Profile"
//     }
// }

// function saveProfile(results) {
//     if (document.querySelector('#to-disable').disabled){
//         document.querySelector('#to-disable').disabled = true;
//         document.querySelector('.profile-button').innerText = "Edit Profile";
//     }
//   }

// document.querySelector('.profile-button').addEventListener('click', evt => {
//     evt.preventDefault();
  
//     const formInputs = {
//       fname: document.querySelector('#fname-field').value,
//     //   lname: document.querySelector('#lname-field').value,
//     //   address1: document.querySelector('#address1-field').value,
//     //   address2: document.querySelector('#address2-field').value,
//     //   city: document.querySelector('#city-field').value,
//     //   state: document.querySelector('#state-field').value,
//     //   zip: document.querySelector('#zip-field').value,
//     //   phone: document.querySelector('#phone-field').value,
//     //   about_me: document.querySelector('#aboutme-field').innerText,
//     //   image: document.querySelector('#image-field').value,
//     };

//     const userId = document.querySelector('#userid-field"').value
    
//     console.log(formInputs)
//     fetch(`/user/${userId}/edit, {
//       method: 'POST',
//       body: JSON.stringify(formInputs),
//       headers: {
//         'Content-Type': 'application/json',
//       },
//     })
//       .then(response => response.json())
//       .then(responseJson => {
//         console.log(responseJson);
//       });
// });



//   // So you'll use JS to grab the values from all your inputs, and send an AJAX request to your server. 
// // When that completes, you can change the fieldset disabled back to true, and the button text back to "Edit Profile"




