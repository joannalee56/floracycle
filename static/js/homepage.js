// 'use strict';

// function initMap() {

//     const postalCode = document.querySelector('#zip').value;
//     const miles = document.querySelector('#miles').value;

//     const geocoder = new google.maps.Geocoder();
//     geocoder.geocode({address: postalCode}, (results, status) => {
//         if (status === 'OK') {
//         // Get the coordinates of the user's location
//         const userLocation = results[0].geometry.location;
        
//         // const map = new google.maps.Map(document.querySelector('#map'), {
//         //   center: userLocation,
//         //   zoom: 18,
//         // });
//         console.log(userLocation);
//         // map.setCenter(userLocation);
//         // map.setZoom(13);
//         } else {
//         alert(`Geocode was unsuccessful for the following reason: ${status}`);
//         }
//     });

// //DISTANCE MATRIX QUERY
//     const service = new google.maps.DistanceMatrixService();
//     service.getDistanceMatrix({
//          origins: userLocation,
//          destinations: postalCode,
//          unitSystem:   miles
//     }, function(response, status) {
//         if(status == google.maps.DistanceMatrixStatus.OK) {
//               const origins = response.originAddresses;
//               const destinations = response.destinationAddresses;
//               const miles = response.elements.distance    
//     }      
// }); 
// }   


// }

