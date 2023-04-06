from App.database import db
from datetime import datetime


class ProductQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_name = db.Column(db.String(256), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product_name = db.Column(db.String(256), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    farmer_name = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(1024), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, user_name, product_id, product_name, farmer_id, farmer_name, phone, email, message):
        self.user_id = user_id
        self.user_name = user_name
        self.product_id = product_id
        self.product_name = product_name
        self.farmer_id = farmer_id
        self.farmer_name = farmer_name
        self.phone = phone
        self.email = email
        self.message = message
        self.timestamp = datetime.now()

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "farmer_id": self.farmer_id,
            "farmer_name": self.farmer_name,
            "phone": self.phone,
            "email": self.email,
            "message": self.message,
            "timestamp": self.timestamp,
        }
