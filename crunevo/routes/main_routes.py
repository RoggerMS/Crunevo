from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    current_app,
    jsonify,
    session,
)
from flask_login import login_required, current_user
from crunevo.extensions import db
from crunevo.models.note import Note
from crunevo.models.post import Post
from crunevo.utils.storage import save_file_local
from crunevo.utils.cloudinary_upload import upload_image
from crunevo.utils.ia import fetch_cohere_advice
from datetime import date, datetime

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        notes = Note.query.order_by(Note.created_at.desc()).limit(10).all()
        posts = Post.query.order_by(Post.timestamp.desc()).limit(10).all()
        items = sorted(posts + notes, key=lambda x: x.created_at, reverse=True)
        return render_template(
            "feed.html",
            items=items,
            user=current_user,
            now=datetime.utcnow(),
        )
    return render_template("index.html")


@main_bp.route("/ranking")
def ranking():
    return render_template("ranking.html")


@main_bp.route("/feed")
def feed_redirect():
    return redirect(url_for("main.index"))


@main_bp.route("/about")
def about():
    """Página informativa sobre el proyecto."""
    return render_template("about.html")


@main_bp.route("/crear_post", methods=["POST"])
@login_required
def crear_post():
    content = request.form.get("content") or request.form.get("text_post") or ""
    content = content.strip()
    image = request.files.get("image")

    if not content and (not image or not image.filename):
        flash("Escribe algo o agrega una imagen.", "warning")
        return redirect(url_for("main.index"))

    image_url = None
    try:
        if image and image.filename:
            image_url = upload_image(image)

        post = Post(content=content, image_url=image_url, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error al crear post: {e}", exc_info=True)
        db.session.rollback()
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"error": "Error al guardar"}), 500
        flash("Ocurrió un error al guardar la publicación.", "danger")
        return redirect(url_for("main.index"))

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(
            {
                "message": "ok",
                "post": {
                    "content": post.content,
                    "image_url": post.image_url,
                    "user_name": current_user.name,
                    "user_career": current_user.career or "",
                },
            }
        )

    flash("Publicación creada.", "success")
    return redirect(url_for("main.index"))


@main_bp.route("/api/ia/consejo")
@login_required
def ia_consejo():
    today = date.today().isoformat()
    last = session.get("ia_date")
    count = session.get("ia_count", 0)
    if last != today:
        session["ia_date"] = today
        count = 0
    if count >= 3:
        return jsonify({"mensaje": "Límite diario alcanzado. Consigue CRUNEVO+"})

    session["ia_count"] = count + 1
    mensaje = fetch_cohere_advice()
    return jsonify({"mensaje": mensaje})
