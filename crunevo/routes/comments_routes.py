from flask import Blueprint, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from crunevo.models import db
from crunevo.models.comment import Comment
from crunevo.models.note import Note
from crunevo.models.post import Post
from crunevo.models.post_comment import PostComment
from crunevo.models.user import User

comment_bp = Blueprint("comments", __name__)


@comment_bp.route("/comments/add", methods=["POST"])
@login_required
def add_comment():
    content = request.form.get("content", "").strip()
    note_id = request.form.get("note_id", type=int)

    if not content:
        flash("El comentario no puede estar vacío.", "warning")
        return redirect(url_for("note.note_detail", note_id=note_id))

    note = Note.query.get_or_404(note_id)
    comment = Comment(content=content, note_id=note.id, user_id=current_user.id)
    db.session.add(comment)
    db.session.commit()
    flash("Comentario publicado.", "success")
    return redirect(url_for("note.note_detail", note_id=note.id))


@comment_bp.route("/comments/delete/<int:id>", methods=["POST"])
@login_required
def delete_comment(id: int):
    comment = Comment.query.get_or_404(id)
    if comment.user_id != current_user.id:
        flash("No puedes eliminar este comentario.", "danger")
        return redirect(url_for("note.note_detail", note_id=comment.note_id))

    db.session.delete(comment)
    db.session.commit()
    flash("Comentario eliminado.", "success")
    return redirect(url_for("note.note_detail", note_id=comment.note_id))


@comment_bp.route("/comments/like/<int:id>", methods=["POST"])
@login_required
def like_comment(id: int):
    comment = Comment.query.get_or_404(id)
    if comment.user_id == current_user.id:
        flash("No puedes dar like a tu propio comentario.", "warning")
        return redirect(url_for("note.note_detail", note_id=comment.note_id))

    comment.likes = (comment.likes or 0) + 1
    if comment.likes == 5:
        user = db.session.get(User, comment.user_id)
        if user:
            user.credits = (user.credits or 0) + 2
    db.session.commit()
    return redirect(url_for("note.note_detail", note_id=comment.note_id))


@comment_bp.route("/posts/<int:post_id>/comment", methods=["POST"])
@login_required
def comment_post(post_id: int):
    content = request.form.get("content", "").strip()
    if not content:
        return jsonify({"error": "empty"}), 400
    post = Post.query.get_or_404(post_id)
    new_comment = PostComment(content=content, post_id=post.id, user_id=current_user.id)
    db.session.add(new_comment)
    db.session.commit()
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"message": "ok"})
    flash("Comentario publicado.", "success")
    return redirect(url_for("main.index"))
