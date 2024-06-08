from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GameType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rules = db.relationship('Rule', backref='game_type', lazy=True)
    files = db.relationship('UploadedFile', backref='game_type', lazy=True)

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300), nullable=False)
    filepath = db.Column(db.String(300), nullable=False)
    uploaded_on = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    processed = db.Column(db.Boolean, default=False)
    game_type_id = db.Column(db.Integer, db.ForeignKey('game_type.id'), nullable=False)

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    game_type_id = db.Column(db.Integer, db.ForeignKey('game_type.id'), nullable=False)
