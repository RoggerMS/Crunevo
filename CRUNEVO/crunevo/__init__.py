
from flask import Flask
from flask_login import LoginManager
from .models import db
from .models.user import User as _User
from .models.note import (
    Note as _Note,
    Download as _Download,
    Like as _Like,
    Report as _Report,
)
from .models.product import Product as _Product
from .models.forum import Pregunta as _Pregunta, Respuesta as _Respuesta

# Expose models without underscores for ease of use across the package
User = _User
Note = _Note
Download = _Download
Like = _Like
Report = _Report
Product = _Product
Pregunta = _Pregunta
Respuesta = _Respuesta
from .routes.main_routes import main_bp
from .routes.auth_routes import auth_bp
from .routes.store_routes import store_bp
from .routes.note_routes import note_bp

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(store_bp)
    app.register_blueprint(note_bp)

    return app
