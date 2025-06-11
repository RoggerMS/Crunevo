from datetime import datetime
from crunevo.extensions import db


class LoginLog(db.Model):
    __tablename__ = "login_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    success = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    device_type = db.Column(db.String(50))
    method = db.Column(db.String(50))

    user = db.relationship("User", backref="login_logs")

    def __repr__(self):
        return f"<LoginLog user_id={self.user_id} success={self.success}>"
