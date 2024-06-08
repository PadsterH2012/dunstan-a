from ai_utils import generate_scenario, process_command

def get_initial_scenario():
    return generate_scenario()

def handle_user_command(command):
    return process_command(command)
