# models/forum.py
from datetime import datetime
from app import db

class Pregunta(db.Model):
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    respuestas = db.relationship('Respuesta', backref='pregunta', lazy=True)

class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
