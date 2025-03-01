const statusLabel = document.getElementById('statusLabel');

document.getElementById('pressButton').addEventListener('click', () => {
    fetch('/press_button')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            statusLabel.textContent = `Status: ${data.message}`;
        })
        .catch(error => {
            console.error('Error:', error);
            statusLabel.textContent = 'Status: Error';
        });
});

document.getElementById('holdButton').addEventListener('mousedown', () => {
    fetch('/hold_button')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            statusLabel.textContent = `Status: ${data.message}`;
        })
        .catch(error => {
            console.error('Error:', error);
            statusLabel.textContent = 'Status: Error';
        });
});

document.getElementById('holdButton').addEventListener('mouseup', () => {
    fetch('/release_button')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            statusLabel.textContent = `Status: ${data.message}`;
        })
        .catch(error => {
            console.error('Error:', error);
            statusLabel.textContent = 'Status: Error';
        });
});

