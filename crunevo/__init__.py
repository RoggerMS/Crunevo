
from flask import Flask
from flask_login import LoginManager
from crunevo.models import db
from crunevo.models.user import User as _User
from crunevo.models.note import (
    Note as _Note,
    Download as _Download,
    Like as _Like,
    Report as _Report,
)
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
from crunevo.routes.main_routes import main_bp
from crunevo.routes.auth_routes import auth_bp
from crunevo.routes.store_routes import store_bp
from crunevo.routes.note_routes import note_bp

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config.from_object("crunevo.config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))

    with app.app_context():
        from sqlalchemy.exc import OperationalError

        try:
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

    return app
