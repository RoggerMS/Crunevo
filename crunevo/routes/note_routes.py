from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
    send_from_directory,
)
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime
import os

from crunevo.utils.storage import allowed_file, upload_file_to_s3, save_file_local

from crunevo.models import db
from crunevo.models.note import Note
from crunevo.models.user import User

note_bp = Blueprint("note", __name__)

# --- Configuración AWS S3 ---
S3_BUCKET = os.environ.get("S3_BUCKET_NAME", "your-s3-bucket-name-placeholder")


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
                Note.title.ilike(f"%{search_term}%")
                | Note.description.ilike(f"%{search_term}%")
                | Note.course.ilike(f"%{search_term}%")
                | Note.tags.ilike(f"%{search_term}%")
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
            faculty_filter=faculty_filter,
        )

    except Exception as e:
        current_app.logger.error(f"Error en /apuntes: {e}", exc_info=True)
        flash("Ocurrió un error al cargar los apuntes.", "danger")
        return render_template(
            "notes_section.html",
            notes=[],
            pagination=None,
            search_term="",
            faculty_filter=[],
        )


# --- Ruta: Subir Apunte ---
@note_bp.route("/subir", methods=["GET", "POST"])
@note_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_note():
    if request.method == "POST":
        user_id = current_user.id

        title = request.form.get("title")
        faculty = request.form.get("faculty")
        course = request.form.get("course")
        description = request.form.get("description")
        tags = request.form.get("tags")
        note_file = request.files.get("note_file")
        filename = secure_filename(note_file.filename) if note_file else ""
        terms_accepted = request.form.get("terms")

        if not all([title, faculty, course, note_file, terms_accepted]):
            flash(
                "Completa todos los campos requeridos y acepta los términos.", "danger"
            )
            return render_template("upload_note.html", form_data=request.form)

        if note_file and allowed_file(filename):
            note_file.filename = filename
            note_file.seek(0, os.SEEK_END)
            size_mb = note_file.tell() / (1024 * 1024)
            note_file.seek(0)
            if size_mb > current_app.config["MAX_NOTE_FILE_SIZE_MB"]:
                flash("El archivo supera el tamaño máximo permitido.", "danger")
                return render_template("upload_note.html", form_data=request.form)

            file_url = None
            if S3_BUCKET and S3_BUCKET != "your-s3-bucket-name-placeholder":
                file_url = upload_file_to_s3(note_file, S3_BUCKET)

            if not file_url:
                file_url = save_file_local(
                    note_file, current_app.config["NOTE_UPLOAD_FOLDER"]
                )

            if file_url:
                try:
                    file_type = filename.rsplit(".", 1)[1].lower()
                    new_note = Note(
                        title=title,
                        description=description,
                        file_url=file_url,
                        file_type=file_type,
                        user_id=user_id,
                        course=course,
                        faculty=faculty,
                        tags=tags,
                        upload_date=datetime.utcnow(),
                    )

                    user = User.query.get(user_id)
                    if user:
                        user.credits = (user.credits or 0) + 10

                    db.session.add(new_note)
                    db.session.commit()

                    flash("Apunte subido exitosamente.", "success")
                    return redirect(url_for("note.notes_section"))

                except Exception as e:
                    db.session.rollback()
                    current_app.logger.error(
                        f"Error al guardar apunte: {e}", exc_info=True
                    )
                    flash(
                        "Ocurrió un error al guardar el apunte en la base de datos.",
                        "danger",
                    )
            else:
                flash("Ocurrió un error al guardar el archivo.", "danger")
                current_app.logger.error("No se pudo obtener la URL del archivo")
        else:
            flash("Solo se permiten archivos PDF, DOCX o PNG.", "danger")

    return render_template("upload_note.html")


@note_bp.route("/notes/<int:note_id>/download")
def download_note_file(note_id: int):
    note = Note.query.get_or_404(note_id)
    if note.file_url.startswith(current_app.static_url_path):
        rel_path = note.file_url.replace(current_app.static_url_path + "/", "")
        return send_from_directory(
            current_app.static_folder, rel_path, as_attachment=True
        )
    return redirect(note.file_url)


@note_bp.route("/nota/<int:note_id>")
def note_detail(note_id: int):
    """Display a single note with an embedded preview if possible."""
    note = Note.query.get_or_404(note_id)
    return render_template("note_detail.html", note=note)
