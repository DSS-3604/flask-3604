from App.database import db
from datetime import datetime
from App.models.user import User


class FarmerReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # foreign key links to farmer.id in farmer table
    farmer_name = db.Column(db.String(120), nullable=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # foreign key links to user.id in user table
    user_name = db.Column(db.String(120), nullable=True)
    rating = db.Column(db.Integer, nullable=False)  # rating of farmer
    body = db.Column(db.String(1024), nullable=False)  # body of comment
    timestamp = db.Column(db.DateTime, nullable=False)  # timestamp of comment
    updated_timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, farmer_id, farmer_name, user_id, user_name, user_avatar, rating, body):
        self.farmer_id = farmer_id
        self.farmer_name = farmer_name
        self.user_id = user_id
        self.user_name = user_name
        self.rating = rating
        self.body = body
        self.timestamp = datetime.now()
        self.updated_timestamp = datetime.now()
        self.user_avatar = user_avatar

    def to_json(self):
        return {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "farmer_name": self.farmer_name,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "body": self.body,
            "timestamp": self.timestamp,
            "updated_timestamp": self.updated_timestamp,
        }
