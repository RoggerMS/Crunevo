from datetime import datetime
from crunevo.extensions import db


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    file_url = db.Column(db.String(512), nullable=False)
    file_type = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    course = db.Column(db.String(100))
    faculty = db.Column(db.String(100))
    tags = db.Column(db.Text)  # Simple text field for tags initially
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    likes_count = db.Column(db.Integer, default=0)
    downloads_count = db.Column(db.Integer, default=0)
    is_reported = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    uploader = db.relationship("User", back_populates="notes")
    download_records = db.relationship(
        "Download", back_populates="note", lazy=True, cascade="all, delete-orphan"
    )
    like_records = db.relationship(
        "Like", back_populates="note", lazy=True, cascade="all, delete-orphan"
    )
    report_records = db.relationship(
        "Report", back_populates="note", lazy=True, cascade="all, delete-orphan"
    )

    @property
    def page_count(self):
        """Return the number of pages for PDF notes if available."""
        if self.file_type != "pdf" or not self.file_url:
            return None
        try:
            import os
            import fitz  # PyMuPDF
            from flask import current_app

            if self.file_url.startswith(current_app.static_url_path):
                rel = self.file_url.replace(current_app.static_url_path + "/", "")
                path = os.path.join(current_app.static_folder, rel)
            else:
                path = self.file_url

            with fitz.open(path) as doc:
                return doc.page_count
        except Exception:
            return None

    def __repr__(self):
        return f"<Note {self.title}>"


class Download(db.Model):
    __tablename__ = "downloads"
    __table_args__ = (
        db.UniqueConstraint("user_id", "note_id", name="uq_user_note_download"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey("notes.id"), nullable=False)
    download_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("User", back_populates="downloads")
    note = db.relationship("Note", back_populates="download_records")


class Like(db.Model):
    __tablename__ = "likes"
    __table_args__ = (
        db.UniqueConstraint("user_id", "note_id", name="uq_user_note_like"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey("notes.id"), nullable=False)
    like_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("User", back_populates="likes")
    note = db.relationship("Note", back_populates="like_records")


class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey("notes.id"), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # User who reported
    reason = db.Column(db.Text, nullable=False)
    report_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(
        db.String(20), default="pending"
    )  # 'pending', 'reviewed', 'resolved'

    # Relationships
    reporter = db.relationship("User", back_populates="reports")
    note = db.relationship("Note", back_populates="report_records")
