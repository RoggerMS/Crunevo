from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Central extensions so they can be imported without circular dependencies

db = SQLAlchemy()
login_manager = LoginManager()
