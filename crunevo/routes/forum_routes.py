from flask import Blueprint, render_template, request, redirect, url_for, flash
from crunevo.models.forum import Pregunta, Respuesta
from crunevo.models import db
from flask_login import login_required, current_user

forum_bp = Blueprint("forum", __name__, url_prefix="/foro")


@forum_bp.route("/")
def foro():
    page = request.args.get("page", 1, type=int)
    pagination = Pregunta.query.order_by(Pregunta.fecha_creacion.desc()).paginate(
        page=page, per_page=10
    )
    return render_template(
        "foro/foro.html", preguntas=pagination.items, pagination=pagination
    )


@forum_bp.route("/<int:pregunta_id>")
@forum_bp.route("/pregunta/<int:pregunta_id>")
def ver_pregunta(pregunta_id):
    pregunta = Pregunta.query.get_or_404(pregunta_id)
    respuestas = (
        Respuesta.query.filter_by(pregunta_id=pregunta_id)
        .order_by(Respuesta.fecha.desc())
        .all()
    )
    return render_template(
        "foro/ver_pregunta.html", pregunta=pregunta, respuestas=respuestas
    )


@forum_bp.route("/nueva", methods=["GET", "POST"])
@login_required
def nueva_pregunta():
    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        contenido = request.form["contenido"].strip()
        if len(titulo) < 5 or len(contenido) < 20:
            flash(
                "El título debe tener al menos 5 caracteres y el contenido 20.",
                "danger",
            )
            return redirect(url_for("forum.nueva_pregunta"))
        nueva = Pregunta(titulo=titulo, contenido=contenido, autor_id=current_user.id)
        db.session.add(nueva)
        db.session.commit()
        flash("Pregunta publicada con éxito.", "success")
        return redirect(url_for("forum.foro"))
    return render_template("foro/nueva_pregunta.html")


@forum_bp.route("/<int:pregunta_id>/responder", methods=["POST"])
@login_required
def responder(pregunta_id):
    contenido = request.form["contenido"].strip()
    if len(contenido) < 20:
        flash("La respuesta debe tener al menos 20 caracteres.", "danger")
        return redirect(url_for("forum.ver_pregunta", pregunta_id=pregunta_id))
    respuesta = Respuesta(
        contenido=contenido, autor_id=current_user.id, pregunta_id=pregunta_id
    )
    db.session.add(respuesta)
    db.session.commit()
    flash("Respuesta enviada.", "success")
    return redirect(url_for("forum.ver_pregunta", pregunta_id=pregunta_id))
