'use strict';

function initMap() {
  
  const postalCode = document.querySelector('.postal_code').innerText;
  const geocoder = new google.maps.Geocoder();
  geocoder.geocode({address: postalCode}, (results, status) => {
      if (status === 'OK') {
      // Get the coordinates of the user's location
      const userLocation = results[0].geometry.location;
      
      const map = new google.maps.Map(document.querySelector('#map'), {
        center: userLocation,
        zoom: 18,
      });

      console.log(results)
      console.log(userLocation)
      
      // Create a marker
      // new google.maps.Marker({
      //     position: userLocation,
      //     map,
      // });

      // Zoom in on the geolocated location
      map.setCenter(userLocation);
      map.setZoom(13);
      } else {
      alert(`Geocode was unsuccessful for the following reason: ${status}`);
      }
  });
}



