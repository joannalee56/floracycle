document.querySelector('.btn-primary').addEventListener('submit', evt => {
    evt.preventDefault();
  
    const formInputs = {
      post_title: document.querySelector('#title').value,
      description: document.querySelector('#description').value,
      cost: document.querySelector('#cost').value,
      cost_type: document.querySelector('#cost_type').value,
      postal_code: document.querySelector('#postal_code').value,
      post_image: document.querySelector('#post_image').value,
    };

    fetch('/classified/new', {
      method: 'POST',
      body: JSON.stringify(formInputs),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => response.json())
      .then(responseJson => {
        saveProfile;
      });
});

function saveProfile(results) {
    if (document.querySelector('#to-disable').disabled){
        document.querySelector('#to-disable').disabled = true;
        document.querySelector('.profile-button').innerText = "Edit Profile";
    }
  }



