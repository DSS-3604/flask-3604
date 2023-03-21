from App.database import db
import datetime
from App.models.user import User


class FarmerApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comment = db.Column(db.String(1024), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(
        self,
        user_id,
        comment="",
    ):
        self.user_id = user_id
        self.status = "Pending"
        self.comment = comment
        self.timestamp = datetime.datetime.now()

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": User.query.filter_by(id=self.user_id).first().username,
            "status": self.status,
            "comment": self.comment,
            "timestamp": self.timestamp,
        }
