from App.database import db
import secrets


class FarmerApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.String(1024), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    currency = db.Column(db.String(120), nullable=True)
    units = db.Column(db.String(10), nullable=True)
    avatar = db.Column(db.String(120), nullable=True)

    def __init__(self, username, email, bio, phone, address, currency="USD", units="kg", avatar=""):
        self.status = "Pending"
        self.username = username
        self.password = secrets.token_urlsafe(32)
        self.email = email
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
        }
