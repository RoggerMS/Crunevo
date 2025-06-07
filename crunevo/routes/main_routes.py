
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from crunevo.models.note import Note

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.feed'))
    return render_template('index.html')


@main_bp.route('/ranking')
def ranking():
    return render_template('ranking.html')


@main_bp.route('/feed')
@login_required
def feed():
    notes = Note.query.order_by(Note.upload_date.desc()).limit(20).all()
    return render_template('feed.html', notes=notes, user=current_user)


@main_bp.route('/about')
def about():
    """Página informativa sobre el proyecto."""
    return render_template('about.html')
