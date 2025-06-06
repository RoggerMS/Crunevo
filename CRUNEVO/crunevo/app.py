from flask import Flask
from crunevo.routes.main_routes import main_bp
from crunevo.routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('crunevo.config.Config')
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    return app
