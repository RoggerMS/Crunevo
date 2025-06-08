from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from crunevo.models.note import Note

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        notes = Note.query.order_by(Note.downloads_count.desc()).limit(10).all()
        posts = [
            {
                "uploader": current_user,
                "content": "¡Bienvenido al nuevo feed social de CRUNEVO!",
                "image_url": None,
            },
            {
                "uploader": current_user,
                "content": "Comparte tus mejores tips de estudio.",
                "image_url": None,
            },
        ]
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
