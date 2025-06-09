from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from crunevo.models import db
import logging

# Crear el blueprint para las rutas de usuario
user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/profile")
@login_required
def profile():
    """Display the profile of the logged in user."""
    # Obtener apuntes subidos y registros relacionados
    uploaded_notes = current_user.notes
    download_history = current_user.downloads

    # Calcular estadísticas clave
    notes_uploaded = len(uploaded_notes)
    downloads_total = sum(note.downloads_count or 0 for note in uploaded_notes)
    likes_received = sum(note.likes_count or 0 for note in uploaded_notes)
    responses_count = len(current_user.respuestas)
    points = current_user.points or 0

    user_stats = {
        "notes_uploaded": notes_uploaded,
        "downloads_total": downloads_total,
        "likes_received": likes_received,
        "responses_count": responses_count,
        "points": points,
    }

    # Construir feed de actividad reciente
    events = []
    for note in uploaded_notes:
        events.append(
            {
                "timestamp": note.upload_date,
                "message": f'\ud83d\udce4 Subiste el apunte "{note.title}"',
            }
        )
        if note.downloads_count:
            events.append(
                {
                    "timestamp": note.upload_date,
                    "message": f'\u2b07\ufe0f Tu apunte "{note.title}" fue descargado {note.downloads_count} veces',
                }
            )
    for r in current_user.respuestas:
        events.append(
            {
                "timestamp": r.fecha,
                "message": f'\ud83d\udcac Respondiste a la pregunta "{r.pregunta.titulo}"',
            }
        )
    for p in getattr(current_user, "posts", []):
        events.append(
            {
                "timestamp": p.timestamp,
                "message": "\ud83d\udce3 Publicaste una actualizaci\u00f3n",
            }
        )

    events.sort(key=lambda e: e["timestamp"], reverse=True)

    # Determinar nivel del usuario basado en créditos
    user_level = "Novato"  # Placeholder
    if current_user.credits > 1000:
        user_level = "Experto"
    elif current_user.credits > 100:
        user_level = "Ayudante"

    return render_template(
        "perfil.html",
        user=current_user,
        user_stats=user_stats,
        user_level=user_level,
        events=events,
    )


@user_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    # Obtener el usuario autenticado
    user = current_user

    if request.method == "POST":
        # Obtener datos del formulario
        user.name = request.form.get("name", user.name)
        user.faculty = request.form.get("faculty", user.faculty)
        user.career = request.form.get("career", user.career)
        user.study_year = request.form.get("study_year", user.study_year)
        user.bio = request.form.get("bio", user.bio)
        # TODO: agregar soporte para actualizar foto de perfil

        try:
            db.session.commit()
            flash("Perfil actualizado exitosamente.", "success")
            return redirect(url_for("user.profile"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar el perfil: {e}", "danger")
            logging.exception("Error al actualizar el perfil")

    # Prellenar el formulario para la solicitud GET
    return render_template("edit_profile.html", user=user)


@user_bp.route("/notes")
@login_required
def my_notes():
    """Display notes uploaded by the current user."""
    uploaded_notes = current_user.notes
    return render_template("my_notes.html", notes=uploaded_notes)
