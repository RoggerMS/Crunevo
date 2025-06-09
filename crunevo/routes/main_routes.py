from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    current_app,
    jsonify,
)
import os
from flask_login import login_required, current_user
from crunevo.models import db
from crunevo.models.note import Note
from crunevo.models.post import Post
from crunevo.utils.storage import save_file_local

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        notes = Note.query.order_by(Note.downloads_count.desc()).limit(10).all()
        posts = Post.query.order_by(Post.timestamp.desc()).limit(10).all()
        return render_template("feed.html", notes=notes, posts=posts, user=current_user)
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
    if image and image.filename:
        upload_folder = os.path.join(current_app.static_folder, "uploads", "posts")
        os.makedirs(upload_folder, exist_ok=True)
        image_url = save_file_local(image, upload_folder)

    post = Post(content=content, image_url=image_url, user_id=current_user.id)
    db.session.add(post)
    db.session.commit()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(
            {
                "message": "ok",
                "post": {
                    "content": post.content,
                    "image_url": post.image_url,
                    "user_name": current_user.name,
                    "user_career": current_user.career,
                },
            }
        )

    flash("Publicación creada.", "success")
    return redirect(url_for("main.index"))
