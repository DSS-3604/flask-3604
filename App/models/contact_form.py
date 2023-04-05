from App.database import db
from datetime import datetime


class ContactForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(1024), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(
        self,
        name,
        phone,
        email,
        message
    ):
        self.name = name
        self.phone = phone
        self.email = email
        self.message = message
        self.timestamp = datetime.now()

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "message": self.message,
            "timestamp": self.timestamp
        }