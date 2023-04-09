from App.database import db
from datetime import datetime


class ProductComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=False
    )  # foreign key links to product.id in product table
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # foreign key links to user.id in user table
    user_name = db.Column(db.String(120), nullable=True)
    body = db.Column(db.String(1024), nullable=False)  # body of comment
    timestamp = db.Column(db.DateTime, nullable=False)  # timestamp of comment
    updated_timestamp = db.Column(db.DateTime, nullable=False)
    p_replies = db.relationship(
        "ProductReply",
        backref="product_comment",
        lazy=True,
        cascade="all, delete-orphan",
    )  # replies to comment

    def __init__(self, product_id, user_id, user_name, body):
        self.product_id = product_id
        self.user_id = user_id
        self.user_name = user_name
        self.body = body
        self.timestamp = datetime.now()
        self.updated_timestamp = datetime.now()

    def to_json(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "body": self.body,
            "timestamp": self.timestamp,
            "updated_timestamp": self.updated_timestamp,
        }
