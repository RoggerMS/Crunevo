from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from crunevo.extensions import db

# Use scrypt to hash all stored passwords
PASSWORD_HASH_METHOD = "scrypt"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100))
    faculty = db.Column(db.String(100))
    career = db.Column(db.String(100))
    study_year = db.Column(db.String(50))
    bio = db.Column(db.Text)
    profile_picture_url = db.Column(db.String(512))
    role = db.Column(db.String(20), default="user")
    credits = db.Column(db.Integer, default=0)
    chat_enabled = db.Column(db.Boolean, default=False)
    points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_banned = db.Column(db.Boolean, default=False)

    # Relationships
    notes = db.relationship(
        "Note", back_populates="uploader", lazy=True, cascade="all, delete-orphan"
    )
    downloads = db.relationship(
        "Download", back_populates="user", lazy=True, cascade="all, delete-orphan"
    )
    likes = db.relationship(
        "Like", back_populates="user", lazy=True, cascade="all, delete-orphan"
    )
    reports = db.relationship(
        "Report", back_populates="reporter", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, password: str) -> None:
        """Store a hashed password using scrypt."""
        if password.startswith(f"{PASSWORD_HASH_METHOD}:"):
            raise ValueError("Password must be plain text, not a pre-generated hash")
        self.password = generate_password_hash(password, method=PASSWORD_HASH_METHOD)

    def check_password(self, password: str) -> bool:
        """Validate a plain password against the stored hash."""
        return check_password_hash(self.password, password)
