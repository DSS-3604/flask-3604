from flask_jwt import JWT
from App.models import User
from App.controllers import get_user_by_username


def authenticate(username, password):
    user = get_user_by_username(username)
    if user and user.check_password(password):
        return user
    return None


# Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
    return User.query.get(payload["identity"])


def setup_jwt(app):
    return JWT(app, authenticate, identity)
