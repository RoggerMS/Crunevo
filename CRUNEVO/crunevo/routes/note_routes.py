from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

from ..models import db
from ..models.note import Note
from ..models.user import User

note_bp = Blueprint("note", __name__)

# --- Configuración AWS S3 ---
S3_BUCKET = os.environ.get("S3_BUCKET_NAME", "your-s3-bucket-name-placeholder")
S3_REGION = os.environ.get("AWS_REGION", "us-east-1")
S3_BASE_URL = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/"
s3_client = boto3.client("s3", region_name=S3_REGION)

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "doc", "docx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    filename = secure_filename(file.filename)
    try:
        s3_client.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
        return f"{S3_BASE_URL}{filename}"
    except (NoCredentialsError, ClientError, Exception) as e:
        flash("Ocurrió un error al subir el archivo.", "danger")
        current_app.logger.error(f"Error al subir archivo a S3: {e}", exc_info=True)
        return None

# --- Ruta: Explorar Apuntes ---
@note_bp.route("/apuntes")
def notes_section():
    try:
        page = request.args.get("page", 1, type=int)
        search_term = request.args.get("search", "")
        faculty_filter = request.args.getlist("faculty")

        query = Note.query.order_by(Note.upload_date.desc())

        if search_term:
            query = query.filter(
                Note.title.ilike(f"%{search_term}%") |
                Note.description.ilike(f"%{search_term}%") |
                Note.course.ilike(f"%{search_term}%") |
                Note.tags.ilike(f"%{search_term}%")
            )

        if faculty_filter:
            query = query.filter(Note.faculty.in_(faculty_filter))

        pagination = query.paginate(page=page, per_page=10, error_out=False)
        notes = pagination.items

        return render_template(
            "notes_section.html",
            notes=notes,
            pagination=pagination,
            search_term=search_term,
            faculty_filter=faculty_filter
        )

    except Exception as e:
        current_app.logger.error(f"Error en /apuntes: {e}", exc_info=True)
        flash("Ocurrió un error al cargar los apuntes.", "danger")
        return render_template(
            "notes_section.html",
            notes=[],
            pagination=None,
            search_term="",
            faculty_filter=[]
        )

# --- Ruta: Subir Apunte ---
@note_bp.route("/subir", methods=["GET", "POST"])
def upload_note():
    if request.method == "POST":
        user_id = 1  # Usuario simulado por ahora

        title = request.form.get("title")
        faculty = request.form.get("faculty")
        career = request.form.get("career")
        course = request.form.get("course")
        description = request.form.get("description")
        tags = request.form.get("tags")
        note_file = request.files.get("note_file")
        terms_accepted = request.form.get("terms")

        if not all([title, faculty, course, note_file, terms_accepted]):
            flash("Completa todos los campos requeridos y acepta los términos.", "danger")
            return render_template("upload_note.html", form_data=request.form)

        if note_file and allowed_file(note_file.filename):
            file_url = upload_file_to_s3(note_file, S3_BUCKET)

            if file_url:
                try:
                    file_type = note_file.filename.rsplit(".", 1)[1].lower()
                    new_note = Note(
                        title=title,
                        description=description,
                        file_url=file_url,
                        file_type=file_type,
                        user_id=user_id,
                        course=course,
                        faculty=faculty,
                        tags=tags,
                        upload_date=datetime.utcnow()
                    )

                    user = User.query.get(user_id)
                    if user:
                        user.points = (user.points or 0) + 10

                    db.session.add(new_note)
                    db.session.commit()

                    flash("Apunte subido exitosamente.", "success")
                    return redirect(url_for("note.notes_section"))

                except Exception as e:
                    db.session.rollback()
                    current_app.logger.error(f"Error al guardar apunte: {e}", exc_info=True)
                    flash("Ocurrió un error al guardar el apunte en la base de datos.", "danger")
        else:
            flash("Archivo no válido o formato no permitido.", "danger")

    return render_template("upload_note.html")
