from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.forum import Pregunta, Respuesta
from models.user import User
from app import db
from flask_login import login_required, current_user

forum_bp = Blueprint('forum', __name__, url_prefix='/foro')

@forum_bp.route('/')
def foro():
    preguntas = Pregunta.query.order_by(Pregunta.fecha_creacion.desc()).all()
    return render_template('foro/foro.html', preguntas=preguntas)

@forum_bp.route('/pregunta/<int:id>')
def ver_pregunta(id):
    pregunta = Pregunta.query.get_or_404(id)
    return render_template('foro/pregunta.html', pregunta=pregunta)

@forum_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva_pregunta():
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        nueva = Pregunta(titulo=titulo, contenido=contenido, autor_id=current_user.id)
        db.session.add(nueva)
        db.session.commit()
        flash('Pregunta publicada con éxito.', 'success')
        return redirect(url_for('forum.foro'))
    return render_template('foro/nueva_pregunta.html')

@forum_bp.route('/responder/<int:pregunta_id>', methods=['POST'])
@login_required
def responder(pregunta_id):
    contenido = request.form['contenido']
    respuesta = Respuesta(contenido=contenido, autor_id=current_user.id, pregunta_id=pregunta_id)
    db.session.add(respuesta)
    db.session.commit()
    flash('Respuesta enviada.', 'success')
    return redirect(url_for('forum.ver_pregunta', id=pregunta_id))
