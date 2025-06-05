
from flask import Flask
from .models import db
from .routes.main_routes import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    app.register_blueprint(main_bp)

    return app
