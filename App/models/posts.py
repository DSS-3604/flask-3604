from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String, nullable=False)
    description = db.Column(db.String(120), nullable=False)

    def __init__(self, title, description):
        self.title = title
        self.description=description
        
    def get_id(self):
        return self.id
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
        
    def toJSON(self):
        return{
            'title': self.title,
            'description': self.description
        }