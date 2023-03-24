from App.database import db
from datetime import datetime


class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    products = db.relationship(
        "Product", backref="category", lazy=True, cascade="all, delete-orphan"
    )
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, name):
        self.name = name
        self.timestamp = datetime.now()

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "products": [product.to_json() for product in self.products],
        }
