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
    # Obtener los apuntes subidos y el historial de descargas
    uploaded_notes = current_user.notes
    download_history = current_user.downloads

    # Calcular estadísticas del usuario
    user_stats = {
        "notes_uploaded": len(uploaded_notes),
        "notes_downloaded": len(download_history),
        "likes_received": sum(note.likes_count for note in uploaded_notes),
    }

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
        uploaded_notes=uploaded_notes,
        download_history=download_history,
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