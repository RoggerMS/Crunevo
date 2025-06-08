from flask import Flask, render_template, request, redirect, url_for, flash, current_app
import importlib
import os
import crunevo.config as config_module
from flask_login import LoginManager
from crunevo.models import db
from flask_migrate import Migrate
from crunevo.models.user import User as _User
from crunevo.models.note import (
    Note as _Note,
    Download as _Download,
    Like as _Like,
    Report as _Report,
)
from crunevo.models.post import Post as _Post
from crunevo.models.product import Product as _Product
from crunevo.models.forum import Pregunta as _Pregunta, Respuesta as _Respuesta

# Expose models without underscores for ease of use across the package
User = _User
Note = _Note
Download = _Download
Like = _Like
Report = _Report
Product = _Product
Pregunta = _Pregunta
Respuesta = _Respuesta
Post = _Post
from crunevo.routes.main_routes import main_bp
from crunevo.routes.auth_routes import auth_bp
from crunevo.routes.store_routes import store_bp
from crunevo.routes.note_routes import note_bp
from crunevo.routes.forum_routes import forum_bp
from crunevo.routes.user_routes import user_bp
from crunevo.routes.admin_routes import admin_bp

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Debes iniciar sesi\u00f3n para subir apuntes."
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    config = importlib.reload(config_module)
    app.config.from_object(config.Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def handle_unauthorized():
        if request.path in {"/upload", "/subir"}:
            current_app.logger.warning(
                f"Upload attempt without login from {request.remote_addr}"
            )
        flash(
            login_manager.login_message, category=login_manager.login_message_category
        )
        return redirect(url_for(login_manager.login_view, next=request.url))

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))

    with app.app_context():
        from sqlalchemy.exc import OperationalError

        try:
            if not os.getenv("CRUNEVO_NO_CREATE_ALL"):
                db.create_all()
        except OperationalError as exc:
            raise RuntimeError(
                "Failed to initialize the database. Check that the path "
                "specified in SQLALCHEMY_DATABASE_URI is writable and that "
                "DATABASE_DIR points to a directory with write permissions."
            ) from exc

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(store_bp)
    app.register_blueprint(note_bp)
    app.register_blueprint(forum_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("500.html"), 500

    return app
