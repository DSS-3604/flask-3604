import logging
import unittest
from werkzeug.security import generate_password_hash

from App.models import (
    User,
    Product,
    ProductCategory,
    ProductComment,
    ProductReply,
    FarmerReview,
    FarmerApplication,
    ContactForm,
    Logging,
    ProductQuery,
)

LOGGER = logging.getLogger(__name__)

"""
   Unit Tests
"""


class TestUserUnit(unittest.TestCase):
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


class TestProductUnit(unittest.TestCase):
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


class TestProductCategoryUnit(unittest.TestCase):
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


class TestFarmerReviewUnit(unittest.TestCase):
    def test_new_farmer_review(self):
        farmer = User("farmer123", "farmer123@gmail.com", "farmerpass", access="farmer")
        user = User("bob3579", "bob3579@gmail.com", "bobpass")
        review = FarmerReview(
            farmer_id=farmer.id,
            farmer_name=farmer.username,
            user_id=user.id,
            user_name=user.username,
            user_avatar=user.avatar,
            rating=5,
            body="Hello",
        )
        assert review.farmer_id == farmer.id

    def test_farmer_review_attributes(self):
        farmer = User("farmer123", "farmer123@gmail.com", "farmerpass", access="farmer")
        user = User("bob3579", "bob3579@gmail.com", "bobpass")
        review = FarmerReview(
            farmer_id=farmer.id,
            farmer_name=farmer.username,
            user_id=user.id,
            user_name=user.username,
            user_avatar=user.avatar,
            rating=5,
            body="Hello",
        )
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
        review = FarmerReview(
            farmer_id=farmer.id,
            farmer_name=farmer.username,
            user_id=user.id,
            user_name=user.username,
            user_avatar=user.avatar,
            rating=5,
            body="Hello",
        )
        review_json = review.to_json()
        for key, val in review_json.items():
            assert getattr(review, key) == val


class TestFarmerApplicationUnit(unittest.TestCase):
    def test_new_farmer_application(self):
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


class TestContactFormUnit(unittest.TestCase):
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


class TestLoggingUnit(unittest.TestCase):
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


class TestProductQueryUnit(unittest.TestCase):
    def test_create_product_query(self):
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
        user = User(username="bob3579", email="bob3579@gmail.com", password="mypass", access="user", phone="1234567890")
        query = ProductQuery(
            user_id=user.id,
            user_name=user.username,
            product_id=product.id,
            product_name=product.name,
            farmer_id=product.farmer_id,
            farmer_name=product.farmer_name,
            phone=user.phone,
            email=user.email,
            message="Hello",
        )
        assert query.user_id == user.id

    def test_product_query_attributes(self):
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
        user = User(username="bob3579", email="bob3579@gmail.com", password="mypass", access="user", phone="1234567890")
        query = ProductQuery(
            user_id=user.id,
            user_name=user.username,
            product_id=product.id,
            product_name=product.name,
            farmer_id=product.farmer_id,
            farmer_name=product.farmer_name,
            phone=user.phone,
            email=user.email,
            message="Hello",
        )
        assert query.user_id == user.id
        assert query.user_name == user.username
        assert query.product_id == product.id
        assert query.product_name == product.name
        assert query.farmer_id == product.farmer_id
        assert query.farmer_name == product.farmer_name
        assert query.phone == user.phone
        assert query.email == user.email
        assert query.message == "Hello"

    def test_product_query_json(self):
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
        user = User(username="bob3579", email="bob3579@gmail.com", password="mypass", access="user", phone="1234567890")
        query = ProductQuery(
            user_id=user.id,
            user_name=user.username,
            product_id=product.id,
            product_name=product.name,
            farmer_id=product.farmer_id,
            farmer_name=product.farmer_name,
            phone=user.phone,
            email=user.email,
            message="Hello",
        )
        query_json = query.to_json()
        for key, val in query_json.items():
            assert getattr(query, key) == val
