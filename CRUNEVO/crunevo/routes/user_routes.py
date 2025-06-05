from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from src.models import db
from src.models.user import User

# Crear el blueprint para las rutas de usuario
user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/profile")
@login_required
def profile():
    # TODO: Fetch user's uploaded notes and download history
    uploaded_notes = []  # Placeholder: Reemplazar con consulta real
    download_history = []  # Placeholder: Reemplazar con consulta real

    # Calcular estadísticas del usuario
    user_stats = {
        "notes_uploaded": len(uploaded_notes),  # Reemplazar con consulta real
        "notes_downloaded": len(download_history),  # Reemplazar con consulta real
        "likes_received": current_user.likes_received if hasattr(current_user, "likes_received") else 0,
    }

    # Determinar nivel del usuario basado en puntos
    user_level = "Novato"  # Placeholder
    if current_user.points > 1000:
        user_level = "Experto"
    elif current_user.points > 100:
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
        # TODO: Manejar actualización de foto de perfil

        try:
            db.session.commit()
            flash("Perfil actualizado exitosamente.", "success")
            return redirect(url_for("user.profile"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar el perfil: {e}", "danger")
            # TODO: Registrar el error en un log

    # Prellenar el formulario para la solicitud GET
    return render_template("edit_profile.html", user=user)