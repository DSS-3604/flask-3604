from App.database import db
import datetime


class ProductReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"),
                           nullable=False)  # foreign key links to product.id in product table
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),
                        nullable=False)  # foreign key links to user.id in user table
    rating = db.Column(db.Integer, nullable=False)  # rating of review
    body = db.Column(db.String(1024), nullable=False)  # body of review
    timestamp = db.Column(db.DateTime, nullable=False)  # timestamp of review
    p_replies = db.relationship("ProductReply", backref="productreview", lazy=True)  # replies to review

    def __init__(self, rating, product_id, user_id, body):
        self.product_id = product_id
        self.user_id = user_id
        self.rating = rating
        self.body = body
        self.timestamp = datetime.datetime.now()

    def to_json(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "rating": self.rating,
            "body": self.body,
            "timestamp": self.timestamp,
        }
