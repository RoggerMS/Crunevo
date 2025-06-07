
from flask import Blueprint, render_template
from flask_login import login_required
from ..models.note import Note

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/ranking')
def ranking():
    return render_template('ranking.html')


@main_bp.route('/feed')
@login_required
def feed():
    notes = Note.query.order_by(Note.upload_date.desc()).limit(20).all()
    return render_template('feed.html', notes=notes)


@main_bp.route('/about')
def about():
    """Página informativa sobre el proyecto."""
    return render_template('about.html')
