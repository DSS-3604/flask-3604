from App.database import db
from datetime import datetime


class Product(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    farmer_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # foreign key links to user.id in user table
    category_id = db.Column(
        db.Integer, db.ForeignKey("product_category.id"), nullable=False
    )  # foreign key links to product_category.id in product_category table
    name = db.Column(db.String, nullable=False)  # name of product
    description = db.Column(db.String, nullable=False)  # description of product
    image = db.Column(db.String, nullable=False)  # image of product
    retail_price = db.Column(
        db.Float(decimal_return_scale=2), nullable=False
    )  # price of product
    wholesale_price = db.Column(
        db.Float(decimal_return_scale=2), nullable=False
    )  # wholesale price of product
    wholesale_unit_quantity = db.Column(
        db.Integer, nullable=False
    )  # quantity of product for wholesale price
    total_product_quantity = db.Column(db.String, nullable=False)  # unit of product
    comments = db.relationship(
        "ProductComment", backref="product", lazy=True, cascade="all, delete-orphan"
    )  # comments of product
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow
    )  # timestamp of product creation

    def __init__(
        self,
        farmer_id,
        category_id,
        name,
        description,
        image,
        retail_price=1,
        wholesale_price=1,
        wholesale_unit_quantity=1,
        total_product_quantity=1,
    ):
        self.farmer_id = farmer_id
        self.category_id = category_id
        self.name = name
        self.description = description
        self.image = image
        self.retail_price = retail_price
        self.wholesale_price = wholesale_price
        self.wholesale_unit_quantity = wholesale_unit_quantity
        self.total_product_quantity = total_product_quantity

    def to_json(self):
        return {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "retail_price": self.retail_price,
            "wholesale_price": self.wholesale_price,
            "wholesale_unit_quantity": self.wholesale_unit_quantity,
            "total_product_quantity": self.total_product_quantity,
            "comments": [comment.to_json() for comment in self.comments],
        }
