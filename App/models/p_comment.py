from App.database import db
import datetime


class ProductComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"),
                           nullable=False)  # foreign key links to product.id in product table
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),
                        nullable=False)  # foreign key links to user.id in user table
    body = db.Column(db.String(1024), nullable=False)  # body of comment
    timestamp = db.Column(db.DateTime, nullable=False)  # timestamp of comment
    p_replies = db.relationship("ProductReply", backref="product_comment", lazy=True)  # replies to comment

    def __init__(self, product_id, user_id, body):
        self.product_id = product_id
        self.user_id = user_id
        self.body = body
        self.timestamp = datetime.datetime.now()

    def to_json(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "body": self.body,
            "timestamp": self.timestamp,
        }
