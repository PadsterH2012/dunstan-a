import requests

OLLAMA_URL = "http://10.203.20.99:11434/api/generate"
OLLAMA_MODEL = "llama3:8b"

def interpret_rule(rule_text, context):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"You are an AI assistant. Here is the content of a Dungeons & Dragons rulebook: {rule_text} Please interpret the rules and provide guidance based on the context: {context}.",
        "stream": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        output = response.json()
        print(f"Interpret Rule Response: {output}")  # Debug output
        return output.get('response', 'No output returned from OLLAMA.')
    except requests.exceptions.RequestException as e:
        print(f"Error interacting with OLLAMA API: {e}")
        return "Error: Unable to interpret the rule."

def generate_scenario():
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": "Generate a random RPG scenario that introduces the setting and offers multiple choices for the player to start their adventure.",
        "stream": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        output = response.json()
        scenario_text = output.get('response', 'You find yourself in a mysterious place.')

        # Format the response text with HTML
        formatted_text = f"""
            <h3>Scenario</h3>
            <p>{scenario_text}</p>
            <h3>Options</h3>
            <ul>
                <li data-command="option1">Option 1: Follow the cryptic message and search for shadows that seem out of place.</li>
                <li data-command="option2">Option 2: Investigate the strange symbols and see if they hold any clues.</li>
                <li data-command="option3">Option 3: Open the mysterious box and examine its contents.</li>
            </ul>
        """
        print(f"Generate Scenario Response: {output}")  # Debug output
        return formatted_text
    except requests.exceptions.RequestException as e:
        print(f"Error interacting with OLLAMA API: {e}")
        return "Error: Unable to generate a scenario."

def process_command(command):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"You are an AI assistant in an RPG game. The player has given the command: {command}. Respond appropriately.",
        "stream": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        output = response.json()
        print(f"Process Command Response: {output}")  # Debug output
        return output.get('response', f"You decided to: {command}")
    except requests.exceptions.RequestException as e:
        print(f"Error interacting with OLLAMA API: {e}")
        return "Error: Unable to process the command."
