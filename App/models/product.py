from App.database import db
from App.models.user import User
from App.models.product_category import ProductCategory
from datetime import datetime


class Product(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    farmer_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # foreign key links to user.id in user table
    farmer_name = db.Column(db.String, nullable=False)  # name of farmer
    category_id = db.Column(
        db.Integer, db.ForeignKey("product_category.id"), nullable=False
    )  # foreign key links to product_category.id in product_category table
    category_name = db.Column(db.String, nullable=False)  # name of product category
    name = db.Column(db.String, nullable=False)  # name of product
    description = db.Column(db.String, nullable=False)  # description of product
    image = db.Column(
        db.String,
        nullable=False,
        default="https://s3.eu-west-2.amazonaws.com/devo.core.images/products/b1bf55b2-18c6-4184-9522-72b28b13d62d_5054073003722.png",
    )  # image of product
    retail_price = db.Column(
        db.Float(decimal_return_scale=2), nullable=False
    )  # price of product
    wholesale_price = db.Column(
        db.Float(decimal_return_scale=2), nullable=False
    )  # wholesale price of product
    wholesale_unit_quantity = db.Column(
        db.Integer, nullable=False
    )  # quantity of product for wholesale price
    total_product_quantity = db.Column(db.Integer, nullable=False)  # unit of product
    comments = db.relationship(
        "ProductComment", backref="product", lazy=True, cascade="all, delete-orphan"
    )  # comments of product
    timestamp = db.Column(db.DateTime, nullable=False)  # timestamp of product creation
    updated_timestamp = db.Column(
        db.DateTime, nullable=False
    )  # timestamp of product update

    def __init__(
        self,
        farmer_id,
        farmer_name,
        category_id,
        category_name,
        name,
        description,
        image,
        retail_price=1,
        wholesale_price=1,
        wholesale_unit_quantity=1,
        total_product_quantity=1,
    ):
        self.farmer_id = farmer_id
        self.farmer_name = farmer_name
        self.category_id = category_id
        self.category_name = category_name
        self.name = name
        self.description = description
        self.image = image
        self.retail_price = retail_price
        self.wholesale_price = wholesale_price
        self.wholesale_unit_quantity = wholesale_unit_quantity
        self.total_product_quantity = total_product_quantity
        self.timestamp = datetime.now()
        self.updated_timestamp = datetime.now()

    def to_json(self):
        return {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "farmer_name": self.farmer_name,
            "category_id": self.category_id,
            "category_name": self.category_name,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "retail_price": self.retail_price,
            "wholesale_price": self.wholesale_price,
            "wholesale_unit_quantity": self.wholesale_unit_quantity,
            "total_product_quantity": self.total_product_quantity,
            "comments": [comment.to_json() for comment in self.comments],
            "timestamp": self.timestamp,
            "updated_timestamp": self.updated_timestamp,
        }
