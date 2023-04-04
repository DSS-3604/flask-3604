import os
import logging
import pytest
import unittest
from werkzeug.security import generate_password_hash, check_password_hash
import time

from App.controllers.auth import authenticate
from App.controllers.user import is_admin
from App.database import create_db
from App.models import User, Product, ProductCategory, ProductComment, ProductReply, FarmerReview, FarmerApplication, ContactForm
from wsgi import app

LOGGER = logging.getLogger(__name__)

"""
   Unit Tests
"""


class UserUnitTests(unittest.TestCase):
    def test_new_user(self):
        user = User("bob3578", "bob3578@gmail.com", "bobpass")
        assert user.username == "bob3578"

    def test_new_admin_user(self):
        user = User("bob3579", "bob3579@gmail.com", "bobpass", access="admin")
        assert user.access == "admin"

    def test_new_normal_user(self):
        user = User("bob3580", "bob3580@gmail.com", "bobpass")
        assert user.access == "user"

    def test_user_is_admin(self):
        user = User("bob3579", "bob3579@gmail.com", "bobpass", access="admin")
        assert user.access == "admin"

    def test_user_is_not_admin(self):
        user = User("bob3579", "bob3579@gmail.com", "bobpass")
        assert user.access != "admin"

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method="sha256")
        user = User("bob3579", "bob3579@gmail.com", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob3579", "bob3579@gmail.com", password)
        assert user.check_password(password)

    def test_correct_password(self):
        user = User("bob3579", "bob3579@gmail.com", "mypass")
        assert user.check_password("mypass")

    def test_incorrect_password(self):
        user = User("bob3579", "bob3579@gmail.com", "mypass")
        assert not user.check_password("wrongpass")




"""
    Integration Tests
"""


# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"})
    create_db(app)
    yield app.test_client()
    os.remove("C:\\Users\\Satyaan\\Desktop\\flask-3604\\App\\test.db")


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert authenticate("bob", "bobpass") != None


class UsersIntegrationTests(unittest.TestCase):
    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual(
            [{"id": 1, "username": "bob"}, {"id": 2, "username": "rick"}], users_json
        )

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
