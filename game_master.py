import random
from models import Rule

def generate_scenario():
    scenarios = [
        "You find yourself in a dark forest. What do you do?",
        "You enter a bustling town. Where do you go?",
        "A dragon blocks your path. How do you proceed?"
    ]
    return random.choice(scenarios)

def process_command(command):
    # Placeholder for command processing logic
    response = f"You decided to: {command}"
    return response
