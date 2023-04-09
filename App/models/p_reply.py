from App.database import db
from datetime import datetime
from App.models.user import User


class ProductReply(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    p_comment_id = db.Column(
        db.Integer, db.ForeignKey("product_comment.id"), nullable=False
    )  # foreign key links to product_comment.id in comment table
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # foreign key links to user.id in user table
    user_name = db.Column(db.String(120), nullable=True)
    body = db.Column(db.String(1024), nullable=False)  # body of reply
    timestamp = db.Column(db.DateTime, nullable=False)  # timestamp of reply
    updated_timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, p_comment_id, user_id, user_name, body):
        self.p_comment_id = p_comment_id
        self.user_id = user_id
        self.user_name = user_name
        self.body = body
        self.timestamp = datetime.now()
        self.updated_timestamp = datetime.now()

    def to_json(self):
        return {
            "id": self.id,
            "p_comment_id": self.p_comment_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "body": self.body,
            "timestamp": self.timestamp,
            "updated_timestamp": self.updated_timestamp,
        }
