from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.note import Note
from app import db
import os
import uuid

notes_bp = Blueprint('notes', __name__, url_prefix='/apuntes')

UPLOAD_FOLDER = 'static/uploads/apuntes'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx', 'txt'}

# Asegurar que exista el directorio de subida
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@notes_bp.route('/')
def listar_apuntes():
    apuntes = Note.query.order_by(Note.fecha_subida.desc()).all()
    return render_template('apuntes/list.html', apuntes=apuntes)

@notes_bp.route('/subir', methods=['GET', 'POST'])
@login_required
def subir_apunte():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        archivo = request.files.get('archivo')

        if not titulo or not archivo:
            flash('Título y archivo son obligatorios.', 'danger')
            return redirect(request.url)

        if archivo and allowed_file(archivo.filename):
            filename = secure_filename(archivo.filename)
            unique_name = f"{uuid.uuid4()}_{filename}"
            archivo_path = os.path.join(UPLOAD_FOLDER, unique_name)
            archivo.save(archivo_path)

            nuevo_apunte = Note(
                titulo=titulo,
                descripcion=descripcion,
                filename=unique_name,
                user_id=current_user.id
            )
            db.session.add(nuevo_apunte)
            db.session.commit()

            flash('Apunte subido correctamente.', 'success')
            return redirect(url_for('notes.listar_apuntes'))
        else:
            flash('Tipo de archivo no permitido. Solo se aceptan PDF, DOCX, PPTX, TXT.', 'warning')
            return redirect(request.url)

    return render_template('apuntes/upload.html')

@notes_bp.route('/ver/<int:apunte_id>')
def ver_apunte(apunte_id):
    apunte = Note.query.get_or_404(apunte_id)
    return render_template('apuntes/detalle.html', apunte=apunte)
