from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db


class User(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    # mandatory fields
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)  # password of user
    access = db.Column(db.String(32), nullable=False)  # access level of user
    currency = db.Column(
        db.String(120), nullable=False, default="USD"
    )  # preferred currency of user
    units = db.Column(
        db.String(10), nullable=False, default="kg"
    )  # preferred units of user
    # optional fields
    bio = db.Column(db.String(1024), nullable=True)  # bio of user
    phone = db.Column(db.String(120), nullable=True)  # phone number of user
    address = db.Column(db.String(120), nullable=True)  # address of user
    avatar = db.Column(db.String(120), nullable=True)  # avatar of user
    # relationships
    p_comments = db.relationship(
        "ProductComment", backref="user", lazy=True
    )  # comments of product
    p_replies = db.relationship(
        "ProductReply", backref="user", lazy=True
    )  # replies to comment
    products = db.relationship(
        "Product", backref="user", lazy=True
    )  # products of farmer
    posted_reviews = db.relationship(
        "FarmerReview",
        backref="posted",
        lazy=True,
        foreign_keys="FarmerReview.farmer_id",
    )  # reviews posted by user
    received_reviews = db.relationship(
        "FarmerReview",
        backref="received",
        lazy=True,
        foreign_keys="FarmerReview.user_id",
    )  # farmer's reviews received
    f_application = db.relationship(
        "FarmerApplication", backref="user", lazy=True
    )  # farmer application of user

    def __init__(
        self,
        username,
        email,
        password,
        access="user",
        bio="",
        phone="",
        address="",
        currency="USD",
        units="kg",
        avatar="",
    ):
        self.username = username
        self.set_password(password)
        self.email = email
        self.access = access
        self.bio = bio
        self.phone = phone
        self.address = address
        self.currency = currency
        self.units = units
        self.avatar = avatar

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "bio": self.bio,
            "phone": self.phone,
            "address": self.address,
            "currency": self.currency,
            "units": self.units,
            "avatar": self.avatar,
            "access": self.access,
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def get_access(self):
        return self.access
