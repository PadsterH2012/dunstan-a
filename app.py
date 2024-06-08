from flask import Flask, request, render_template, redirect, url_for, jsonify
from models import db, Rule, GameProgress
from extract_text import extract_text_from_pdf
from game_master import generate_scenario, process_command
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rpg.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
db.init_app(app)

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        extracted_text = extract_text_from_pdf(file_path)
        new_rule = Rule(content=extracted_text, category='general')
        db.session.add(new_rule)
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/game')
def game():
    scenario = generate_scenario()
    return render_template('game.html', scenario=scenario)

@app.route('/command', methods=['POST'])
def command():
    user_command = request.json.get('command')
    response = process_command(user_command)
    return jsonify(response=response)

@app.route('/playerinfo')
def player_info():
    # This would return the player information; placeholder for now
    return jsonify(player_name="Player", level=1, health=100, inventory=["Sword", "Shield"])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
