'use strict';

// function initMap() {
//   const sfBayCoords = {
//     lat: 37.601773,
//     lng: -122.20287,
//   };

//   const basicMap = new google.maps.Map(document.querySelector('#map'), {
//     center: sfBayCoords,
//     zoom: 12,
//   });

//   }


function initMap() {
    
    const map = new google.maps.Map(document.querySelector('#map'), {
      zoom: 7
      });
    const postalCode = document.querySelector('.postal_code').innerText;
    // Could you reference jinja {{ classified.postal_code }}?

    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({address: postalCode}, (results, status) => {
        if (status === 'OK') {
        // Get the coordinates of the user's location
        const userLocation = results[0].geometry.location;
        
        console.log(results)
        console.log(userLocation)
        
        // Create a marker
        new google.maps.Marker({
            position: userLocation,
            map,
        });
        
        // Zoom in on the geolocated location
        // map.setCenter(userLocation);
        map.setZoom(18);
        } else {
        alert(`Geocode was unsuccessful for the following reason: ${status}`);
        }
    });
}

// function initMap() {
//     const map = new google.maps.Map(document.querySelector('#map'), {
//       center: {
//         lat: 37.601773,
//         lng: -122.20287,
//       },
//       zoom: 11,
//     });
  
//     // Ask user to enter a location. Geocode the location to get its coordinates
//     // and drop a marker onto the map.
//     const postalCode = document.querySelector('.postal_code').innerHTML
  
//       const geocoder = new google.maps.Geocoder();
//       geocoder.geocode({address: userAddress}, (results, status) => {
//         if (status === 'OK') {
//           // Get the coordinates of the user's location
//           const userLocation = results[0].geometry.location;
  
//           // Create a marker
//           new google.maps.Marker({
//             position: userLocation,
//             map,
//           });
  
//           // Zoom in on the geolocated location
//           map.setCenter(userLocation);
//           map.setZoom(18);
//         } else {
//           alert(`Geocode was unsuccessful for the following reason: ${status}`);
//         }
//       });
//   }
  


