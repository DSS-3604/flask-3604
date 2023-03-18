from App.database import db


class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    products = db.relationship("Product", backref="category", lazy=True, cascade="all, delete-orphan")

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "products": [product.to_json() for product in self.products],
        }
