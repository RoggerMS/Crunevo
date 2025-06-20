from datetime import datetime
from crunevo.extensions import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def created_at(self):
        """Alias to unify feed ordering"""
        return self.timestamp

    uploader = db.relationship("User", backref="posts")

    def __repr__(self):
        return f"<Post {self.id}>"
