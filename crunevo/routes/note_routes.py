from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
    send_from_directory,
    jsonify,
)
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime
import os

from crunevo.utils.storage import allowed_file, upload_file_to_s3, save_file_local
from crunevo.utils.cloudinary_upload import upload_image

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
        search_term = request.args.get("search", "").strip()
        faculty_filter = request.args.getlist("faculty")
        course_filter = request.args.get("course", "").strip()
        file_types = request.args.getlist("file_type")
        study_year_filter = request.args.getlist("study_year")

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

        if course_filter:
            query = query.filter(Note.course.ilike(f"%{course_filter}%"))

        if file_types:
            query = query.filter(Note.file_type.in_(file_types))

        if study_year_filter:
            query = query.join(User).filter(User.study_year.in_(study_year_filter))

        pagination = query.paginate(page=page, per_page=10, error_out=False)

        return render_template(
            "notes_section.html",
            notes=pagination,
            search_term=search_term,
            faculty_filter=faculty_filter,
            course_filter=course_filter,
            file_types=file_types,
            study_year_filter=study_year_filter,
        )

    except Exception as e:
        current_app.logger.error(f"Error en /apuntes: {e}", exc_info=True)
        flash("Ocurrió un error al cargar los apuntes.", "danger")
        return render_template(
            "notes_section.html",
            notes=None,
            search_term="",
            faculty_filter=[],
            course_filter="",
            file_types=[],
            study_year_filter=[],
        )


# --- Ruta: Subir Apunte ---
@note_bp.route("/subir", methods=["GET", "POST"])
@note_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_note():
    if request.method == "POST":
        user_id = current_user.id

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        course = request.form.get("course") or request.form.get("categoria")
        faculty = request.form.get("faculty") or course
        tags = request.form.get("tags", "").strip()
        note_file = request.files.get("note_file") or request.files.get("file")
        filename = secure_filename(note_file.filename) if note_file else ""
        terms_accepted = request.form.get("terms")

        if not all([title, note_file, terms_accepted]):
            flash(
                "Completa todos los campos requeridos y acepta los términos.", "danger"
            )
            return render_template("upload_note.html", form_data=request.form)

        if not tags:
            flash("Añade al menos una etiqueta.", "danger")
            return render_template("upload_note.html", form_data=request.form)

        if note_file and allowed_file(filename):
            note_file.filename = filename
            note_file.seek(0, os.SEEK_END)
            size_mb = note_file.tell() / (1024 * 1024)
            note_file.seek(0)
            if size_mb > current_app.config["MAX_NOTE_FILE_SIZE_MB"]:
                flash("El archivo supera el tamaño máximo permitido.", "danger")
                return render_template("upload_note.html", form_data=request.form)

            file_url = upload_image(note_file)
            if (
                not file_url
                and S3_BUCKET
                and S3_BUCKET != "your-s3-bucket-name-placeholder"
            ):
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

                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return jsonify({"message": "ok"})

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


@note_bp.route("/quick_note", methods=["POST"])
@login_required
def quick_note():
    """Handle quick note uploads from the feed via AJAX."""
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    categoria = request.form.get("categoria", "").strip()
    tags = request.form.get("tags", "").strip()
    note_file = request.files.get("file")

    if not title or not note_file:
        return jsonify({"error": "Faltan datos"}), 400

    filename = secure_filename(note_file.filename)
    if not filename.lower().endswith(".pdf"):
        return jsonify({"error": "Formato no permitido"}), 400

    note_file.filename = filename
    upload_folder = current_app.config["NOTE_UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    file_url = upload_image(note_file)
    if not file_url:
        file_url = save_file_local(note_file, upload_folder)

    if not file_url:
        return jsonify({"error": "Error al guardar"}), 500

    new_note = Note(
        title=title,
        description=description,
        file_url=file_url,
        file_type="pdf",
        user_id=current_user.id,
        course=categoria,
        faculty=categoria,
        tags=tags,
        upload_date=datetime.utcnow(),
    )

    try:
        db.session.add(new_note)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error al guardar apunte: {e}", exc_info=True)
        db.session.rollback()
        return jsonify({"error": "Error al guardar"}), 500

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(
            {
                "message": "ok",
                "note": {
                    "id": new_note.id,
                    "title": new_note.title,
                    "description": new_note.description,
                    "file_url": new_note.file_url,
                    "file_type": new_note.file_type,
                    "user_name": current_user.name,
                    "user_career": current_user.career or "",
                },
            }
        )

    flash("Apunte subido.", "success")
    return redirect(url_for("main.index"))


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
