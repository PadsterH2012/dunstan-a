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

    // Fetch the initial scenario after the page has loaded
    fetch('/initial_scenario')
        .then(response => response.json())
        .then(data => {
            console.log("Scenario:", data);  // Debug output
            document.getElementById('narrator-content').innerHTML = data.scenario_text;
            document.getElementById('response').innerHTML = '<h3>Options</h3>' + data.options;
        });

    document.getElementById('send-command').addEventListener('click', function() {
        const command = document.getElementById('command-input').value;
        fetch('/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: command })
        })
        .then(response => response.json())
        .then(data => {
            const responseElement = document.createElement('div');
            responseElement.innerHTML = data.response;
            document.getElementById('response').appendChild(responseElement);
            document.getElementById('command-input').value = '';
            document.getElementById('response').scrollTop = document.getElementById('response').scrollHeight;

            fetch('/update_narrator', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: data.response })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('narrator-content').innerHTML = data.narrator_update;
            });
        });
    });
});
