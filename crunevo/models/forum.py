# models/forum.py
from datetime import datetime
from crunevo.extensions import db
from crunevo.models.user import User


class Pregunta(db.Model):
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    autor = db.relationship("User", backref="preguntas")
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    respuestas = db.relationship("Respuesta", backref="pregunta", lazy=True)


class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    autor = db.relationship("User", backref="respuestas")
    pregunta_id = db.Column(db.Integer, db.ForeignKey("pregunta.id"), nullable=False)
    likes = db.Column(db.Integer, default=0)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
