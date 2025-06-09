from datetime import datetime
from crunevo.models import db


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    note_id = db.Column(db.Integer, db.ForeignKey("notes.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    likes = db.Column(db.Integer, default=0)

    user = db.relationship("User", backref="comments")
    note = db.relationship("Note", backref="comments")
