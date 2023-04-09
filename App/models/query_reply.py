from App.database import db
from datetime import datetime


class QueryReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query_id = db.Column(db.Integer, db.ForeignKey("product_query.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_name = db.Column(db.String(120), nullable=True)
    body = db.Column(db.String(1024), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    updated_timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, query_id, user_id, user_name, body):
        self.query_id = query_id
        self.user_id = user_id
        self.user_name = user_name
        self.body = body
        self.timestamp = datetime.now()
        self.updated_timestamp = datetime.now()

    def to_json(self):
        return {
            "id": self.id,
            "query_id": self.query_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "body": self.body,
            "timestamp": self.timestamp,
            "updated_timestamp": self.updated_timestamp,
        }
