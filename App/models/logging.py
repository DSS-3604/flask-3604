from App.database import db
from datetime import datetime


class Logging(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_name = db.Column(db.String(120), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    action = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(1024), nullable=False)

    def __init__(self, user_id, user_name, action, description):
        self.user_id = user_id
        self.user_name = user_name
        self.timestamp = datetime.now()
        self.action = action
        self.description = description

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "timestamp": self.timestamp,
            "action": self.action,
            "description": self.description
        }

