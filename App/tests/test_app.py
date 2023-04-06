import os
import logging
import pytest
import unittest
from werkzeug.security import generate_password_hash

from App.controllers.auth import authenticate
from App.controllers.user import (
    is_admin,
    is_farmer,
    create_user,
    create_admin,
    update_access,
    get_user_by_email,
    get_user_by_username,
    get_user_by_id,
    get_all_users,
    get_all_farmers,
    get_all_users_json,
    update_user,
    check_password,
)
from App.controllers.farmer_application import (
    create_farmer_application,
    get_farmer_application_by_id,
    get_all_farmer_applications,
    update_farmer_application,
    delete_farmer_application,
    approve_farmer_application,
    reject_farmer_application,
    delete_all_farmer_applications,
    get_all_approved_farmer_applications,
    get_all_rejected_farmer_applications,
    get_all_pending_farmer_applications,
)
from App.controllers.report import get_total_user_count

from App.database import create_db
from App.models import User, Product, ProductCategory, ProductComment, ProductReply, FarmerReview, FarmerApplication, ContactForm, Logging
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

    def test_user_attributes(self):
        user = User(
            username="bob3579",
            email="bob3579@gmail.com",
            password="mypass",
            access="admin",
            bio="I am an admin",
            phone="1234567890",
            address="123 Main St",
            currency="USD",
            units="lbs",
            avatar="avatar.jpg",
        )
        assert user.username == "bob3579"
        assert user.email == "bob3579@gmail.com"
        assert user.access == "admin"
        assert user.bio == "I am an admin"
        assert user.phone == "1234567890"
        assert user.address == "123 Main St"
        assert user.currency == "USD"
        assert user.units == "lbs"
        assert user.avatar == "avatar.jpg"

    def test_user_json(self):
        user = User(
            username="bob3579",
            email="bob3579@gmail.com",
            password="mypass",
            access="admin",
            bio="I am an admin",
            phone="1234567890",
            address="123 Main St",
            currency="USD",
            units="lbs",
            avatar="avatar.jpg",
        )
        user_json = user.to_json()
        for key, val in user_json.items():
            assert getattr(user, key) == val


class ProductUnitTests(unittest.TestCase):
    def test_new_product(self):
        farmer = User("farmer123", "farmer123@gmail.com", "farmerpass", access="farmer")
        pc = ProductCategory("Vegetables")
        product = Product(
            farmer_id=farmer.id,
            farmer_name=farmer.username,
            category_id=pc.id,
            category_name=pc.name,
            name="Tomatoes",
            description="Fresh Tomatoes",
            image="tomatoes.jpg",
            retail_price=2.99,
            wholesale_price=1.99,
            wholesale_unit_quantity=10,
            total_product_quantity=100,
        )
        assert product.name == "Tomatoes"

    def test_product_attributes(self):
        farmer = User("farmer123", "farmer123@gmail.com", "farmerpass", access="farmer")
        pc = ProductCategory("Vegetables")
        product = Product(
            farmer_id=farmer.id,
            farmer_name=farmer.username,
            category_id=pc.id,
            category_name=pc.name,
            name="Tomatoes",
            description="Fresh Tomatoes",
            image="tomatoes.jpg",
            retail_price=2.99,
            wholesale_price=1.99,
            wholesale_unit_quantity=10,
            total_product_quantity=100,
        )
        assert product.farmer_id == farmer.id
        assert product.farmer_name == farmer.username
        assert product.category_id == pc.id
        assert product.category_name == pc.name
        assert product.name == "Tomatoes"
        assert product.description == "Fresh Tomatoes"
        assert product.image == "tomatoes.jpg"
        assert product.retail_price == 2.99
        assert product.wholesale_price == 1.99
        assert product.wholesale_unit_quantity == 10
        assert product.total_product_quantity == 100

    def test_product_json(self):
        farmer = User("farmer123", "farmer123@gmail.com", "farmerpass", access="farmer")
        pc = ProductCategory("Vegetables")
        product = Product(
            farmer_id=farmer.id,
            farmer_name=farmer.username,
            category_id=pc.id,
            category_name=pc.name,
            name="Tomatoes",
            description="Fresh Tomatoes",
            image="tomatoes.jpg",
            retail_price=2.99,
            wholesale_price=1.99,
            wholesale_unit_quantity=10,
            total_product_quantity=100,
        )
        product_json = product.to_json()
        for key, val in product_json.items():
            assert getattr(product, key) == val

    def test_product_comments(self):
        farmer = User("farmer123", "farmer123@gmail.com", "farmerpass", access="farmer")
        pc = ProductCategory("Vegetables")
        product = Product(
            farmer_id=farmer.id,
            farmer_name=farmer.username,
            category_id=pc.id,
            category_name=pc.name,
            name="Tomatoes",
            description="Fresh Tomatoes",
            image="tomatoes.jpg",
            retail_price=2.99,
            wholesale_price=1.99,
            wholesale_unit_quantity=10,
            total_product_quantity=100,
        )
        comment = ProductComment(product_id=product.id, user_id=farmer.id, user_name=farmer.username, body="Hello")
        assert comment.product_id == product.id

    def test_product_comment_json(self):
        farmer = User("farmer123", "farmer123@gmail.com", "farmerpass", access="farmer")
        pc = ProductCategory("Vegetables")
        product = Product(
            farmer_id=farmer.id,
            farmer_name=farmer.username,
            category_id=pc.id,
            category_name=pc.name,
            name="Tomatoes",
            description="Fresh Tomatoes",
            image="tomatoes.jpg",
            retail_price=2.99,
            wholesale_price=1.99,
            wholesale_unit_quantity=10,
            total_product_quantity=100,
        )
        comment = ProductComment(product_id=product.id, user_id=farmer.id, user_name=farmer.username, body="Hello")
        comment_json = comment.to_json()
        for key, val in comment_json.items():
            assert getattr(comment, key) == val

    def test_product_comment_replies(self):
        farmer = User("farmer123", "farmer123@gmail.com", "farmerpass", access="farmer")
        pc = ProductCategory("Vegetables")
        product = Product(
            farmer_id=farmer.id,
            farmer_name=farmer.username,
            category_id=pc.id,
            category_name=pc.name,
            name="Tomatoes",
            description="Fresh Tomatoes",
            image="tomatoes.jpg",
            retail_price=2.99,
            wholesale_price=1.99,
            wholesale_unit_quantity=10,
            total_product_quantity=100,
        )
        comment = ProductComment(product_id=product.id, user_id=farmer.id, user_name=farmer.username, body="Hello")
        reply = ProductReply(p_comment_id=comment.id, user_id=farmer.id, user_name=farmer.username, body="Hello self")
        assert reply.p_comment_id == comment.id

    def test_product_reply_json(self):
        farmer = User("farmer123", "farmer123@gmail.com", "farmerpass", access="farmer")
        pc = ProductCategory("Vegetables")
        product = Product(
            farmer_id=farmer.id,
            farmer_name=farmer.username,
            category_id=pc.id,
            category_name=pc.name,
            name="Tomatoes",
            description="Fresh Tomatoes",
            image="tomatoes.jpg",
            retail_price=2.99,
            wholesale_price=1.99,
            wholesale_unit_quantity=10,
            total_product_quantity=100,
        )
        comment = ProductComment(product_id=product.id, user_id=farmer.id, user_name=farmer.username, body="Hello")
        reply = ProductReply(p_comment_id=comment.id, user_id=farmer.id, user_name=farmer.username, body="Hello self")
        reply_json = reply.to_json()
        for key, val in reply_json.items():
            assert getattr(reply, key) == val


class ProductCategoryUnitTests(unittest.TestCase):
    def test_new_product_category(self):
        pc = ProductCategory("Vegetables")
        assert pc.name == "Vegetables"

    def test_product_category_attributes(self):
        pc = ProductCategory("Vegetables")
        assert pc.name == "Vegetables"

    def test_product_category_json(self):
        pc = ProductCategory("Vegetables")
        pc_json = pc.to_json()
        for key, val in pc_json.items():
            assert getattr(pc, key) == val


class FarmerReviewUnitTests(unittest.TestCase):
    def test_new_farmer_review(self):
        farmer = User("farmer123", "farmer123@gmail.com", "farmerpass", access="farmer")
        user = User("bob3579", "bob3579@gmail.com", "bobpass")
        review = FarmerReview(farmer_id=farmer.id, farmer_name=farmer.username, user_id=user.id, user_name=user.username, user_avatar=user.avatar, rating=5, body="Hello")
        assert review.farmer_id == farmer.id

    def test_farmer_review_attributes(self):
        farmer = User("farmer123", "farmer123@gmail.com", "farmerpass", access="farmer")
        user = User("bob3579", "bob3579@gmail.com", "bobpass")
        review = FarmerReview(farmer_id=farmer.id, farmer_name=farmer.username, user_id=user.id,
                              user_name=user.username, user_avatar=user.avatar, rating=5, body="Hello")
        assert review.farmer_id == farmer.id
        assert review.farmer_name == farmer.username
        assert review.user_id == user.id
        assert review.user_name == user.username
        assert review.user_avatar == user.avatar
        assert review.rating == 5
        assert review.body == "Hello"

    def test_farmer_review_json(self):
        farmer = User("farmer123", "farmer123@gmail.com", "farmerpass", access="farmer")
        user = User("bob3579", "bob3579@gmail.com", "bobpass")
        review = FarmerReview(farmer_id=farmer.id, farmer_name=farmer.username, user_id=user.id,
                              user_name=user.username, user_avatar=user.avatar, rating=5, body="Hello")
        review_json = review.to_json()
        for key, val in review_json.items():
            assert getattr(review, key) == val


class FarmerApplicationUnitTests(unittest.TestCase):
    def new_farmer_application_test(self):
        user = User("bob3579", "bob3579@gmail.com", "bobpass")
        application = FarmerApplication(user_id=user.id, user_name=user.username, comment="Hello")
        assert application.user_id == user.id

    def test_farmer_application_attributes(self):
        user = User("bob3579", "bob3579@gmail.com", "bobpass")
        application = FarmerApplication(user_id=user.id, user_name=user.username, comment="Hello")
        assert application.user_id == user.id
        assert application.user_name == user.username
        assert application.comment == "Hello"

    def test_farmer_application_json(self):
        user = User("bob3579", "bob3579@gmail.com", "bobpass")
        application = FarmerApplication(user_id=user.id, user_name=user.username, comment="Hello")
        application_json = application.to_json()
        for key, val in application_json.items():
            assert getattr(application, key) == val


class ContactFormUnitTests(unittest.TestCase):
    def test_new_contact_form(self):
        form = ContactForm(name="Bob", phone="1234567890", email="bob@gmail.com", message="Hello")
        assert form.name == "Bob"

    def test_contact_form_attributes(self):
        form = ContactForm(name="Bob", phone="1234567890", email="bob@gmail.com", message="Hello")
        assert form.name == "Bob"
        assert form.phone == "1234567890"
        assert form.email == "bob@gmail.com"
        assert form.message == "Hello"

    def test_contact_form_json(self):
        form = ContactForm(name="Bob", phone="1234567890", email="bob@gmail.com", message="Hello")
        form_json = form.to_json()
        for key, val in form_json.items():
            assert getattr(form, key) == val


class LoggingUnitTests(unittest.TestCase):
    def test_create_log(self):
        user = User("bob3579", "bob3579@gmail.com", "bobpass")
        log = Logging(user.id, user.username, "Test Log", "Test Log Description")
        assert log.user_id == user.id

    def test_log_attributes(self):
        user = User("bob3579", "bob3579@gmail.com", "bobpass")
        log = Logging(user.id, user.username, "Test Log", "Test Log Description")
        assert log.user_id == user.id
        assert log.action == "Test Log"
        assert log.description == "Test Log Description"

    def test_log_json(self):
        user = User("bob3579", "bob3579@gmail.com", "bobpass")
        log = Logging(user.id, user.username, "Test Log", "Test Log Description")
        log_json = log.to_json()
        for key, val in log_json.items():
            assert getattr(log, key) == val



"""
    Integration Tests
"""


# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and reused for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"})
    create_db(app)
    yield app.test_client()
    # os.remove(os.getcwd().replace("tests", "\\test.db"))


class AuthIntegrationTests(unittest.TestCase):
    def test_authenticate(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password="robpass")
        assert authenticate(f"rob{count}", f"robpass") is not None

    def test_authenticate_invalid(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password="robpass")
        assert authenticate(f"rob{count}", "robpass123") is None


class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password="robpass")
        assert user.username == f"rob{count}"

    def test_create_admin(self):
        count = get_total_user_count()
        admin = create_admin(username=f"admin{count}", email=f"admin{count}@gmail.com", password="adminpass")
        assert admin.username == f"admin{count}"
        assert is_admin(admin)

    def test_get_all_users_json(self):
        users = get_all_users()
        users_json = get_all_users_json()
        self.assertListEqual(
            [user.to_json() for user in users], users_json
        )

    def test_update_user_access(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password=f"robpass")
        update_access(user.id, "admin")
        assert is_admin(user)

    def test_get_user_by_email(self):
        count = get_total_user_count()
        create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password=f"robpass")
        user = get_user_by_email(f"rob{count}@gmail.com")
        assert user.username == f"rob{count}"

    def test_get_user_by_username(self):
        count = get_total_user_count()
        create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password=f"robpass")
        user = get_user_by_username(f"rob{count}")
        assert user.email == f"rob{count}@gmail.com"

    def test_get_user_by_id(self):
        count = get_total_user_count()
        user1 = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password=f"robpass")
        user2 = get_user_by_id(user1.id)
        assert user2 is not None

    def test_get_all_farmers(self):
        farmers = get_all_farmers()
        for farmer in farmers:
            assert is_farmer(farmer)

    # Tests data changes in the database
    def test_update_user(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password=f"robpass")
        with self.subTest("Update username"):
            user1 = update_user(user.id, username=f"tob{count}")
            assert user1.username == f"tob{count}"
        with self.subTest("Update email"):
            user1 = update_user(user.id, email=f"tob{count}@gmail.com")
            assert user1.email == f"tob{count}@gmail.com"
        with self.subTest("Update password"):
            user1 = update_user(user.id, password=f"tobpass1")
            assert check_password(user1, f"tobpass1")
        with self.subTest("Update Bio"):
            user1 = update_user(user.id, bio="Hello World")
            assert user1.bio == "Hello World"
        with self.subTest("Update Phone"):
            user1 = update_user(user.id, phone="9876543210")
            assert user1.phone == "9876543210"
        with self.subTest("Update Address"):
            user1 = update_user(user.id, address="POS")
            assert user1.address == "POS"
        with self.subTest("Update Currency"):
            user1 = update_user(user.id, currency="TTD")
            assert user1.currency == "TTD"
        with self.subTest("Update Units"):
            user1 = update_user(user.id, units="lbs")
            assert user1.units == "lbs"
        with self.subTest("Update avatar"):
            user1 = update_user(user.id, avatar=f"tob{count}.png")
            assert user1.avatar == f"tob{count}.png"


class FarmerApplicationIntegrationTests(unittest.TestCase):
    def test_create_farmer_application(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password=f"robpass")
        application = create_farmer_application(user.id, "I want to be a farmer")
        assert application.user_id == user.id

    def test_get_farmer_application_by_id(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password=f"robpass")
        application = create_farmer_application(user.id, "I want to be a farmer")
        application1 = get_farmer_application_by_id(application.id)
        assert application1 is not None

    def test_get_all_farmer_applications(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password=f"robpass")
        application = create_farmer_application(user.id, "I want to be a farmer")
        applications = get_all_farmer_applications()
        assert application in applications

    def update_farmer_application(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password=f"robpass")
        application = create_farmer_application(user.id, "I want to be a farmer")
        application1 = update_farmer_application(application.id, "I really want to be a farmer")
        assert application1.message == "I really want to be a farmer"

    def test_delete_farmer_application(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password=f"robpass")
        application = create_farmer_application(user.id, "I want to be a farmer")
        delete_farmer_application(application.id)
        application1 = get_farmer_application_by_id(application.id)
        assert application1 is None

    def test_approve_farmer_application(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password=f"robpass")
        application = create_farmer_application(user.id, "I want to be a farmer")
        approve_farmer_application(application.id)
        application1 = get_farmer_application_by_id(application.id)
        assert application1.status == "Approved"

    def test_reject_farmer_application(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password=f"robpass")
        application = create_farmer_application(user.id, "I want to be a farmer")
        reject_farmer_application(application.id)
        application1 = get_farmer_application_by_id(application.id)
        assert application1.status == "Rejected"

    def test_delete_all_farmer_applications(self):
        delete_all_farmer_applications()
        applications = get_all_farmer_applications()
        assert len(applications) == 0

    def test_get_all_approved_farmer_applications(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password=f"robpass")
        application = create_farmer_application(user.id, "I want to be a farmer")
        approve_farmer_application(application.id)
        application1 = get_farmer_application_by_id(application.id)
        applications = get_all_approved_farmer_applications()
        assert application1 in applications

    def test_get_all_rejected_farmer_applications(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password=f"robpass")
        application = create_farmer_application(user.id, "I want to be a farmer")
        reject_farmer_application(application.id)
        application1 = get_farmer_application_by_id(application.id)
        applications = get_all_rejected_farmer_applications()
        assert application1 in applications

    def test_get_all_pending_farmer_applications(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password=f"robpass")
        application = create_farmer_application(user.id, "I want to be a farmer")
        applications = get_all_pending_farmer_applications()
        assert application in applications

