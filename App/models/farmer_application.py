from App.database import db
from datetime import datetime
from App.models.user import User


class FarmerApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_name = db.Column(db.String(120), nullable=True)
    comment = db.Column(db.String(1024), nullable=True)
    created_timestamp = db.Column(db.DateTime, nullable=False)
    updated_timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(
        self,
        user_id,
        user_name,
        comment="",
    ):
        self.user_id = user_id
        self.user_name = user_name
        self.status = "Pending"
        self.comment = comment
        self.created_timestamp = datetime.now()
        self.updated_timestamp = datetime.now()

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "status": self.status,
            "comment": self.comment,
            "created_timestamp": self.created_timestamp,
            "updated_timestamp": self.updated_timestamp,
        }
