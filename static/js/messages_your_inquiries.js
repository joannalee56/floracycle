'use strict';

// Add current time to first chat bubble
let today = new Date();

let hours = today.getHours();
let minutes = today.getMinutes();

// Check whether AM or PM
var newformat = hours >= 12 ? 'PM' : 'AM'; 

// Find current hour in AM-PM Format
hours = hours % 12; 

// To display "0" as "12"
hours = hours ? hours : 12; 
minutes = minutes < 10 ? '0' + minutes : minutes;

let now = (today.getMonth()+1) + '/' + today.getDate() + '/' + today.getFullYear() + " " + hours + ':' + minutes + ' ' + newformat;

document.getElementById("currentDate").innerHTML = now;


// Classified Title to appear on Inbox Page
document.querySelector('#message').addEventListener('submit', evt => {
    evt.preventDefault();

    // Make fetch request to send to server, POST request
    // Also send classified info to add to Messages table

    // document.querySelector('#message-field').value = "Hi, is this available?"
    const message = document.querySelector('#message-field').value;
    if( message !== '' ) {

        const formInputs = {
            message: message,
        };

        // empty the input field
        $( 'input.message' ).val( '' ).focus()

        fetch(`/classified/${classified_id}/send/message`, {
            method: 'POST',
            body: JSON.stringify(formInputs),
            headers: {
            'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                    $( 'div.message_holder' ).append(`<li class="chat-right"><div class="chat-hour">${data.message_time }<span class="fa fa-check-circle"></span></div><div class="chat-text">${data.message}</div><div class="chat-avatar"><img src="${data.db_user.image}"><div class="chat-name">${data.db_user.fname}</div></div></li>`)
            });
        }
});


// For Messages written by Inquirer
document.querySelector('#message').addEventListener('submit', evt => {
    evt.preventDefault();

    // Make fetch request to send to server, POST request
    // Also send classified info to add to Messages table

    // document.querySelector('#message-field').value = "Hi, is this available?"
    const message = document.querySelector('#message-field').value;
    if( message !== '' ) {

        const formInputs = {
            message: message,
        };

        // empty the input field
        $( 'input.message' ).val( '' ).focus()

        fetch(`/classified/${classified_id}/send/message`, {
            method: 'POST',
            body: JSON.stringify(formInputs),
            headers: {
            'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                    $( 'div.message_holder' ).append(`<li class="chat-right"><div class="chat-hour">${data.message_time }<span class="fa fa-check-circle"></span></div><div class="chat-text">${data.message}</div><div class="chat-avatar"><img src="${data.db_user.image}"><div class="chat-name">${data.db_user.fname}</div></div></li>`)
            });
        }
});



// function initMap() {
  
//   const postalCode = document.querySelector('.postal_code').innerText;
//   const geocoder = new google.maps.Geocoder();
//   geocoder.geocode({address: postalCode}, (results, status) => {
//       if (status === 'OK') {
//       // Get the coordinates of the user's location
//       const userLocation = results[0].geometry.location;
      
//       const map = new google.maps.Map(document.querySelector('#map'), {
//         center: userLocation,
//         zoom: 18,
//       });

//       console.log(results)
//       console.log(userLocation)

//       // Zoom in on the geolocated location
//       map.setCenter(userLocation);
//       map.setZoom(13);
//       } else {
//       alert(`Geocode was unsuccessful for the following reason: ${status}`);
//       }
//   });
// }



