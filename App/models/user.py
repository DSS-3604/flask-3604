from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
import datetime


class User(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    access = db.Column(db.String(32), nullable=False)
    currency = db.Column(
        db.String(120), nullable=False, default="USD"
    )
    units = db.Column(
        db.String(10), nullable=False, default="kg"
    )
    bio = db.Column(db.String(1024), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(120), nullable=True)
    avatar = db.Column(db.String(120), nullable=True)
    # comments posted by user
    p_comments = db.relationship(
        "ProductComment", backref="user", lazy=True
    )
    # replies posted by user
    p_replies = db.relationship(
        "ProductReply", backref="user", lazy=True
    )
    # products posted by user
    products = db.relationship(
        "Product", backref="user", lazy=True
    )
    # reviews posted by user
    posted_reviews = db.relationship(
        "FarmerReview",
        backref="posted",
        lazy=True,
        foreign_keys="FarmerReview.farmer_id",
    )
    # reviews received by user
    received_reviews = db.relationship(
        "FarmerReview",
        backref="received",
        lazy=True,
        foreign_keys="FarmerReview.user_id",
    )
    # applications posted by user
    f_application = db.relationship(
        "FarmerApplication", backref="user", lazy=True
    )
    # timestamp of user creation
    timestamp = db.Column(db.DateTime, nullable=False)  # date created

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
        self.timestamp = datetime.datetime.now()

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
            "timestamp": self.timestamp,
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def get_access(self):
        return self.access
