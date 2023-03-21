from App.database import db
import datetime
from App.models.user import User


class FarmerReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # foreign key links to farmer.id in farmer table

    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # foreign key links to user.id in user table
    rating = db.Column(db.Integer, nullable=False)  # rating of farmer
    body = db.Column(db.String(1024), nullable=False)  # body of comment
    timestamp = db.Column(db.DateTime, nullable=False)  # timestamp of comment

    def __init__(self, farmer_id, user_id, rating, body):
        self.farmer_id = farmer_id
        self.user_id = user_id
        self.rating = rating
        self.body = body
        self.timestamp = datetime.datetime.now()

    def to_json(self):
        return {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "farmer_name": User.query.filter_by(id=self.farmer_id).first().username,
            "user_id": self.user_id,
            "user_name": User.query.filter_by(id=self.user_id).first().username,
            "user_avatar": User.query.filter_by(id=self.user_id).first().avatar,
            "rating": self.rating,
            "body": self.body,
            "timestamp": self.timestamp,
        }
