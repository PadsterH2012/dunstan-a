from flask import Flask, request, render_template, redirect, url_for, jsonify
from models import db, Rule, UploadedFile, GameType
from extract_text import extract_text_from_pdf, process_text_with_ai
import os
import requests

OLLAMA_URL = "http://10.203.20.99:11434/api/generate"
OLLAMA_MODEL = "llama3:8b-instruct-q8_0"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rpg.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
db.init_app(app)

@app.route('/')
def home():
    game_types = GameType.query.all()
    return render_template('home.html', game_types=game_types)

@app.route('/add_game_type', methods=['POST'])
def add_game_type():
    name = request.form.get('name')
    if name:
        new_game_type = GameType(name=name)
        db.session.add(new_game_type)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete_game_type/<int:id>')
def delete_game_type(id):
    game_type = GameType.query.get_or_404(id)
    db.session.delete(game_type)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/game_type/<int:id>')
def game_type(id):
    game_type = GameType.query.get_or_404(id)
    uploaded_files = UploadedFile.query.filter_by(game_type_id=id).all()
    rules = Rule.query.filter_by(game_type_id=id).all()
    return render_template('game_type.html', game_type=game_type, uploaded_files=uploaded_files, rules=rules)

@app.route('/upload_file/<int:game_type_id>', methods=['POST'])
def upload_file(game_type_id):
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    new_file = UploadedFile(filename=file.filename, filepath=file_path, game_type_id=game_type_id, processed=False)
    db.session.add(new_file)
    db.session.commit()
    
    return redirect(url_for('game_type', id=game_type_id))

@app.route('/process_file/<int:file_id>', methods=['POST'])
def process_file(file_id):
    uploaded_file = UploadedFile.query.get_or_404(file_id)
    extracted_text = extract_text_from_pdf(uploaded_file.filepath)
    rules = process_text_with_ai(extracted_text)
    for rule in rules:
        new_rule = Rule(content=rule, game_type_id=uploaded_file.game_type_id)
        db.session.add(new_rule)
    
    uploaded_file.processed = True
    db.session.commit()
    
    return redirect(url_for('game_type', id=uploaded_file.game_type_id))

@app.route('/delete_file/<int:id>/<int:game_type_id>')
def delete_file(id, game_type_id):
    uploaded_file = UploadedFile.query.get_or_404(id)
    os.remove(uploaded_file.filepath)
    db.session.delete(uploaded_file)
    db.session.commit()
    return redirect(url_for('game_type', id=game_type_id))

@app.route('/start_game/<int:game_type_id>')
def start_game(game_type_id):
    game_type = GameType.query.get_or_404(game_type_id)
    return render_template('game.html', game_type=game_type.name)

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/initial_scenario', methods=['GET'])
def initial_scenario():
    scenario = get_initial_scenario()
    return jsonify(scenario=scenario)

@app.route('/command', methods=['POST'])
def command():
    user_command = request.json.get('command')
    response = handle_user_command(user_command)
    return jsonify(response=response)

@app.route('/playerinfo')
def player_info():
    return jsonify(player_name="Player", level=1, health=100, inventory=["Sword", "Shield"])

@app.route('/update_narrator', methods=['POST'])
def update_narrator():
    user_command_response = request.json.get('command')
    new_narrator_description = process_narrator_update(user_command_response)
    return jsonify(narrator_update=new_narrator_description)

def get_initial_scenario():
    payload = {
        "model": OLLAMA_MODEL,
        "input": "Generate a random RPG scenario."
    }
    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result.get('response', '')
    else:
        return "Failed to fetch scenario from Ollama."

def handle_user_command(command):
    return "Response to the command"

def process_narrator_update(command_response):
    return f"Updated Narrator Description based on command: {command_response}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

