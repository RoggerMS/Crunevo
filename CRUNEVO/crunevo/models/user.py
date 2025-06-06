from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100))
    role = db.Column(db.String(20), default="user")
    credits = db.Column(db.Integer, default=0)
    chat_enabled = db.Column(db.Boolean, default=False)

    def set_password(self, password: str) -> None:
        """Store a hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Validate a plain password against the stored hash."""
        return check_password_hash(self.password, password)
