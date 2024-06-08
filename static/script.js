document.addEventListener('DOMContentLoaded', function() {
    fetch('/playerinfo')
        .then(response => response.json())
        .then(data => {
            const playerDetails = `
                <p>Name: ${data.player_name}</p>
                <p>Level: ${data.level}</p>
                <p>Health: ${data.health}</p>
                <p>Inventory: ${data.inventory.join(', ')}</p>
            `;
            document.getElementById('player-details').innerHTML = playerDetails;
        });

    document.getElementById('command-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const command = document.getElementById('command-input').value;
        fetch('/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: command })
        })
        .then(response => response.json())
        .then(data => {
            const responseElement = document.createElement('div');
            responseElement.innerText = data.response;
            document.getElementById('response').appendChild(responseElement);
            document.getElementById('command-input').value = '';
        });
    });
});
