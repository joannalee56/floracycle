document.querySelector('#wedding').addEventListener('click', evt => {
    evt.preventDefault();

    fetch('/search/wedding')
    .then(response => response.json())
    .then(responseJson => {
        console.log('this will be logged second');
        document.querySelector('#adjective').innerText = serverData;
    });
    console.log('this will be logged first');



