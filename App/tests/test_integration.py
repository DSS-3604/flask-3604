import logging
import pytest
import unittest
from datetime import datetime, timedelta

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
from App.controllers.report import (
    get_total_user_count,
    get_total_product_count,
    get_total_category_count,
)
from App.controllers.product_category import (
    create_product_category,
    get_product_category_by_id,
    get_product_category_by_id_json,
    update_product_category,
    delete_product_category,
    get_product_category_by_name_json,
    get_product_category_by_name,
    get_product_categories_json,
    get_product_categories,
)
from App.controllers.product import (
    create_product,
    get_product_by_id,
    update_product,
    delete_product,
    get_all_products,
    get_all_products_json,
    get_products_by_farmer_id_json,
    get_products_past_week_json,
    get_products_by_category_id_json,
    search_products_by_name_json,
    search_products_by_name_past_week_json,
)
from App.controllers.contact_form import (
    create_contact_form,
    get_contact_form_by_id,
    get_all_contact_forms,
    get_all_contact_forms_json,
    delete_contact_form_by_id,
    update_contact_form_by_id,
)
from App.controllers.farmer_review import (
    create_review,
    get_all_reviews,
    get_all_reviews_json,
    get_review_by_id,
    get_review_by_id_json,
    get_reviews_by_farmer_id,
    get_reviews_by_farmer_id_json,
    get_reviews_by_user_id,
    get_reviews_by_user_id_json,
    update_review,
    delete_review,
)
from App.controllers.p_comment import (
    create_comment,
    get_all_comments,
    get_all_comments_json,
    get_comment_by_id,
    get_comment_by_id_json,
    get_comments_by_product_id,
    get_comments_by_product_id_json,
    get_comments_by_user_id,
    get_comments_by_user_id_json,
    update_comment,
    delete_comment,
)
from App.controllers.p_reply import (
    create_reply,
    get_all_replies_by_comment_id,
    get_all_replies_by_comment_id_json,
    get_reply_by_id,
    get_reply_by_id_json,
    get_replies_by_user_id,
    get_replies_by_user_id_json,
    update_reply,
    delete_reply,
)
from App.controllers.product_query import (
    create_product_query,
    get_product_query_by_id,
    get_product_query_by_id_json,
    get_all_product_queries,
    get_all_product_queries_json,
    delete_product_query,
    get_product_query_by_user_id_json,
    get_product_query_by_user_id,
    get_product_query_by_product_id_json,
    get_product_query_by_product_id,
    get_product_query_by_farmer_id_json,
    get_product_query_by_farmer_id,
)
from App.controllers.query_reply import (
    create_query_reply,
    get_all_query_replies,
    get_all_query_replies_by_query_id,
    get_all_query_replies_by_query_id_json,
    get_query_reply_by_id,
    get_query_reply_by_id_json,
    get_query_replies_by_user_id,
    get_query_replies_by_user_id_json,
    get_query_replies_by_user_name,
    get_query_replies_by_user_name_json,
    update_query_reply,
    delete_query_reply,
)

from App.controllers.logging import (
    create_log,
    get_all_logs,
    get_all_logs_json,
    get_log_by_id,
    get_log_by_id_json,
    get_logs_by_user_id,
    get_logs_by_user_id_json,
    get_logs_by_action,
    get_logs_by_action_json,
    get_logs_by_user_name,
    get_logs_by_user_name_json,
    get_all_logs_week,
    get_all_logs_week_json,
)


from wsgi import app
from App.models import Product

LOGGER = logging.getLogger(__name__)

"""
    Integration Tests
"""


# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and reused for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"})
    yield app.test_client()


class TestAuthIntegration(unittest.TestCase):
    def test_authenticate(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password="robpass")
        assert authenticate(f"rob{count}", f"robpass") is not None

    def test_authenticate_invalid(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password="robpass")
        assert authenticate(f"rob{count}", "robpass123") is None


class TestUsersIntegration(unittest.TestCase):
    def test_create_user(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password="robpass")
        assert user.username == f"rob{count}"

    def test_create_admin(self):
        count = get_total_user_count()
        admin = create_admin(
            username=f"admin{count}",
            email=f"admin{count}@gmail.com",
            password="adminpass",
        )
        assert admin.username == f"admin{count}"
        assert is_admin(admin)

    def test_get_all_users_json(self):
        users = get_all_users()
        users_json = get_all_users_json()
        self.assertListEqual([user.to_json() for user in users], users_json)

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


class TestFarmerApplicationIntegration(unittest.TestCase):
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

    def test_update_farmer_application(self):
        count = get_total_user_count()
        user = create_user(username=f"rob{count}", email=f"rob{count}@gmail.com", password=f"robpass")
        application = create_farmer_application(user.id, "I want to be a farmer")
        application1 = update_farmer_application(application.id, comment="I really want to be a farmer")
        assert application1.comment == "I really want to be a farmer"

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


class TestProductCategory(unittest.TestCase):
    def test_create_product_category(self):
        count = get_total_category_count()
        category = create_product_category(f"category{count+1}")
        assert category.name == f"category{count+1}"

    def test_get_product_category_by_id(self):
        count = get_total_category_count()
        category = create_product_category(f"category{count+1}")
        category1 = get_product_category_by_id(category.id)
        assert category1 is not None

    def test_get_product_category_by_id_json(self):
        count = get_total_category_count()
        category = create_product_category(f"category{count+1}")
        category1 = get_product_category_by_id_json(category.id)
        assert category1 is not None

    def test_update_product_category(self):
        count = get_total_category_count()
        category = create_product_category(f"category{count+1}")
        category1 = update_product_category(category.id, f"category{count+1}1")
        assert category1.name == f"category{count+1}1"

    def test_delete_product_category(self):
        count = get_total_category_count()
        category = create_product_category(f"category{count+1}")
        delete_product_category(category.id)
        category1 = get_product_category_by_id(category.id)
        assert category1 is None

    def test_get_product_category_by_name_json(self):
        count = get_total_category_count()
        category = create_product_category(f"category{count+1}")
        category1 = get_product_category_by_name_json(category.name)
        assert category1 is not None

    def test_get_product_category_by_name(self):
        count = get_total_category_count()
        category = create_product_category(f"category{count+1}")
        category1 = get_product_category_by_name(category.name)
        assert category1 is not None

    def test_get_all_product_categories(self):
        count = get_total_category_count()
        category = create_product_category(f"category{count+1}")
        categories = get_product_categories()
        assert category in categories

    def test_get_product_categories_json(self):
        count = get_total_category_count()
        category = create_product_category(f"category{count+1}")
        categories = get_product_categories_json()
        assert category.to_json() in categories


class TestProductIntegration(unittest.TestCase):
    ucount = get_total_user_count()
    farmer = create_user(
        username=f"rob{ucount}",
        email=f"rob{ucount}@gmail.com",
        password=f"robpass",
        access="farmer",
    )
    pc_count = get_total_category_count()
    pc = create_product_category(f"category{pc_count + 1}")

    def test_create_product(self):
        pcount = get_total_product_count()
        product = create_product(
            self.farmer.id,
            self.pc.id,
            f"product{pcount}",
            "description",
            "image.jpg",
            10,
            10,
            10,
            10,
        )
        assert product.name == f"product{pcount}"

    def test_get_product_by_id(self):
        pcount = get_total_product_count()
        product = create_product(
            self.farmer.id,
            self.pc.id,
            f"product{pcount}",
            "description",
            "image.jpg",
            10,
            10,
            10,
            10,
        )
        product1 = get_product_by_id(product.id)
        assert product1.name == f"product{pcount}"

    def test_update_product(self):
        pcount = get_total_product_count()
        product = create_product(
            self.farmer.id,
            self.pc.id,
            f"product{pcount}",
            "description",
            "image.jpg",
            10,
            10,
            10,
            10,
        )
        with self.subTest("update category id"):
            pc_count = get_total_category_count()
            pc2 = create_product_category(f"category{pc_count+1}")
            product1 = update_product(id=product.id, category_id=pc2.id)
            assert product1.category_id == pc2.id
        with self.subTest("update name"):
            product1 = update_product(product.id, name=f"product{pcount+1}")
            assert product1.name == f"product{pcount+1}"
        with self.subTest("update description"):
            product1 = update_product(product.id, description="new description")
            assert product1.description == "new description"
        with self.subTest("update image"):
            product1 = update_product(product.id, image="new image.png")
            assert product1.image == "new image.png"
        with self.subTest("update retail_price"):
            product1 = update_product(product.id, retail_price=20)
            assert product1.retail_price == 20
        with self.subTest("update wholesale_price"):
            product1 = update_product(product.id, wholesale_price=20)
            assert product1.wholesale_price == 20
        with self.subTest("update wholesale_unit_quantity"):
            product1 = update_product(product.id, wholesale_unit_quantity=20)
            assert product1.wholesale_unit_quantity == 20
        with self.subTest("update total_product_quantity"):
            product1 = update_product(product.id, total_product_quantity=20)
            assert product1.total_product_quantity == 20

    def test_delete_product(self):
        pcount = get_total_product_count()
        product = create_product(
            self.farmer.id,
            self.pc.id,
            f"product{pcount}",
            "description",
            "image.jpg",
            10,
            10,
            10,
            10,
        )
        delete_product(product.id)
        product1 = get_product_by_id(product.id)
        assert product1 is None

    def test_get_all_products_json(self):
        products = get_all_products()
        products_json = get_all_products_json()
        assert len(products) == len(products_json)
        for product in products:
            assert product.to_json() in products_json

    def test_get_all_products_by_farmer_id_json(self):
        pcount = get_total_product_count()
        product = create_product(
            self.farmer.id,
            self.pc.id,
            f"product{pcount}",
            "description",
            "image.jpg",
            10,
            10,
            10,
            10,
        )
        products = get_products_by_farmer_id_json(self.farmer.id)
        assert product.to_json() in products

    def test_get_products_past_week_json(self):
        products = get_products_past_week_json()
        products2 = Product.query.filter((Product.updated_timestamp >= datetime.now() - timedelta(days=7))).all()
        assert len(products) == len(products2)

    def test_get_products_by_category_json(self):
        products = get_products_by_category_id_json("1")
        products2 = Product.query.filter(Product.category_id == 1).all()
        assert len(products) == len(products2)

    def test_search_products_by_name_json(self):
        pcount = get_total_product_count()
        products = search_products_by_name_json(f"product{pcount-1}")
        products2 = Product.query.filter_by(name=f"product{pcount-1}").all()
        assert len(products) == len(products2)

    def test_search_products_by_name_past_week_json(self):
        pcount = get_total_product_count()
        products = search_products_by_name_past_week_json(f"product{pcount-1}")
        products2 = (
            Product.query.filter_by(name=f"product{pcount-1}")
            .filter((Product.updated_timestamp >= datetime.now() - timedelta(days=7)))
            .all()
        )
        assert len(products) == len(products2)


class TestContactFormIntegration(unittest.TestCase):
    def test_create_contact_form(self):
        contact_form = create_contact_form("name", "phone", "email", "message")
        assert contact_form is not None

    def test_get_contact_form_by_id(self):
        contact_form = create_contact_form("name", "phone", "email", "message")
        contact_form1 = get_contact_form_by_id(contact_form.id)
        assert contact_form1 is not None

    def test_get_all_contact_forms(self):
        contact_form = create_contact_form("name_all", "phone", "email", "message")
        contact_forms = get_all_contact_forms()
        assert contact_form in contact_forms

    def test_get_all_contact_forms_json(self):
        contact_form = create_contact_form("name_all_json", "phone", "email", "message")
        contact_forms = get_all_contact_forms_json()
        assert contact_form.to_json() in contact_forms

    def test_delete_contact_form(self):
        contact_form = create_contact_form("name_delete", "phone", "email", "message")
        delete_contact_form_by_id(contact_form.id)
        contact_form1 = get_contact_form_by_id(contact_form.id)
        assert contact_form1 is None

    def test_update_contact_form(self):
        contact_form = create_contact_form("name_update", "phone", "email", "message")
        contact_form1 = update_contact_form_by_id(
            contact_form.id,
            "name_update",
            "phone_update",
            "email_update",
            "message_update",
        )
        assert contact_form1.name == "name_update"
        assert contact_form1.phone == "phone_update"
        assert contact_form1.email == "email_update"
        assert contact_form1.message == "message_update"


class TestFarmerReviewIntegration(unittest.TestCase):
    ucount = get_total_user_count()
    user = create_user(f"bob{ucount}", f"bob{ucount}", "bobpass")
    farmer = create_user(f"rob{ucount}", f"rob{ucount}", "robpass", "farmer")

    def test_create_review(self):
        review = create_review(self.farmer.id, self.user.id, 5, "review")
        assert review.rating == 5

    def test_get_all_reviews(self):
        review = create_review(self.farmer.id, self.user.id, 5, "reviews")
        reviews = get_all_reviews()
        assert review in reviews

    def test_get_all_reviews_json(self):
        review = create_review(self.farmer.id, self.user.id, 5, "review")
        reviews = get_all_reviews_json()
        assert review.to_json() in reviews

    def test_get_review_by_id(self):
        review = create_review(self.farmer.id, self.user.id, 5, "review")
        review1 = get_review_by_id(review.id)
        assert review1 == review

    def test_get_review_by_id_json(self):
        review = create_review(self.farmer.id, self.user.id, 5, "review")
        review1 = get_review_by_id_json(review.id)
        assert review1 == review.to_json()

    def test_get_reviews_by_farmer_id(self):
        review = create_review(self.farmer.id, self.user.id, 5, "review")
        reviews = get_reviews_by_farmer_id(self.farmer.id)
        assert review in reviews

    def test_get_reviews_by_farmer_id_json(self):
        review = create_review(self.farmer.id, self.user.id, 5, "review")
        reviews = get_reviews_by_farmer_id_json(self.farmer.id)
        assert review.to_json() in reviews

    def test_get_reviews_by_user_id(self):
        review = create_review(self.farmer.id, self.user.id, 5, "review")
        reviews = get_reviews_by_user_id(self.user.id)
        assert review in reviews

    def test_get_reviews_by_user_id_json(self):
        review = create_review(self.farmer.id, self.user.id, 5, "review")
        reviews = get_reviews_by_user_id_json(self.user.id)
        assert review.to_json() in reviews

    def test_update_review(self):
        review = create_review(self.farmer.id, self.user.id, 5, "review")
        review1 = update_review(review.id, 4, "review_update")
        assert review1.rating == 4
        assert review1.body == "review_update"

    def test_delete_review(self):
        review = create_review(self.farmer.id, self.user.id, 5, "review")
        delete_review(review.id)
        review1 = get_review_by_id(review.id)
        assert review1 is None


class TestProductCommentIntegration(unittest.TestCase):
    ucount = get_total_user_count()
    user = create_user(f"bob{ucount}", f"bob{ucount}", "bobpass")
    farmer = create_user(
        username=f"rob{ucount}",
        email=f"rob{ucount}@gmail.com",
        password=f"robpass",
        access="farmer",
    )
    pc_count = get_total_category_count()
    pc = create_product_category(f"category{pc_count + 1}")
    pcount = get_total_product_count()
    product = create_product(farmer.id, pc.id, f"product{pcount}", "description", "image.jpg", 10, 10, 10, 10)

    def test_create_comment(self):
        comment = create_comment(self.product.id, self.user.id, "comment")
        assert comment is not None

    def test_get_all_comments(self):
        comment = create_comment(self.product.id, self.user.id, "comment")
        comments = get_all_comments()
        assert comment in comments

    def test_get_all_comments_json(self):
        comment = create_comment(self.product.id, self.user.id, "comment")
        comments = get_all_comments_json()
        assert comment.to_json() in comments

    def test_get_comment_by_id(self):
        comment = create_comment(self.product.id, self.user.id, "comment")
        comment1 = get_comment_by_id(comment.id)
        assert comment1 == comment

    def test_get_comment_by_id_json(self):
        comment = create_comment(self.product.id, self.user.id, "comment")
        comment1 = get_comment_by_id_json(comment.id)
        assert comment1 == comment.to_json()

    def test_get_comments_by_product_id(self):
        comment = create_comment(self.product.id, self.user.id, "comment")
        comments = get_comments_by_product_id(self.product.id)
        assert comment in comments

    def test_get_comments_by_product_id_json(self):
        comment = create_comment(self.product.id, self.user.id, "comment")
        comments = get_comments_by_product_id_json(self.product.id)
        assert comment.to_json() in comments

    def test_get_comments_by_user_id(self):
        comment = create_comment(self.product.id, self.user.id, "comment")
        comments = get_comments_by_user_id(self.user.id)
        assert comment in comments

    def test_get_comments_by_user_id_json(self):
        comment = create_comment(self.product.id, self.user.id, "comment")
        comments = get_comments_by_user_id_json(self.user.id)
        assert comment.to_json() in comments

    def test_update_comment(self):
        comment = create_comment(self.product.id, self.user.id, "comment")
        comment1 = update_comment(comment.id, "comment_update")
        assert comment1 is not None

    def test_delete_comment(self):
        comment = create_comment(self.product.id, self.user.id, "comment")
        delete_comment(comment.id)
        comment1 = get_comment_by_id(comment.id)
        assert comment1 is None


class TestProductReplyIntegration(unittest.TestCase):
    ucount = get_total_user_count()
    user = create_user(f"bob{ucount}", f"bob{ucount}", "bobpass")
    farmer = create_user(
        username=f"rob{ucount}",
        email=f"rob{ucount}@gmail.com",
        password=f"robpass",
        access="farmer",
    )
    pc_count = get_total_category_count()
    pc = create_product_category(f"category{pc_count + 1}")
    pcount = get_total_product_count()
    product = create_product(farmer.id, pc.id, f"product{pcount}", "description", "image.jpg", 10, 10, 10, 10)
    comment = create_comment(product.id, user.id, "comment")

    def test_create_reply(self):
        reply = create_reply(self.comment.id, self.user.id, "reply")
        assert reply is not None

    def test_get_all_replies_by_comment_id(self):
        reply = create_reply(self.comment.id, self.user.id, "reply")
        replies = get_all_replies_by_comment_id(self.comment.id)
        assert reply in replies

    def test_get_all_replies_by_comment_id_json(self):
        reply = create_reply(self.comment.id, self.user.id, "reply")
        replies = get_all_replies_by_comment_id_json(self.comment.id)
        assert reply.to_json() in replies

    def test_get_reply_by_id(self):
        reply = create_reply(self.comment.id, self.user.id, "reply")
        reply1 = get_reply_by_id(reply.id)
        assert reply1 == reply

    def test_get_reply_by_id_json(self):
        reply = create_reply(self.comment.id, self.user.id, "reply")
        reply1 = get_reply_by_id_json(reply.id)
        assert reply1 == reply.to_json()

    def test_get_replies_by_user_id(self):
        reply = create_reply(self.comment.id, self.user.id, "reply")
        replies = get_replies_by_user_id(self.user.id)
        assert reply in replies

    def test_get_replies_by_user_id_json(self):
        reply = create_reply(self.comment.id, self.user.id, "reply")
        replies = get_replies_by_user_id_json(self.user.id)
        assert reply.to_json() in replies

    def test_update_reply(self):
        reply = create_reply(self.comment.id, self.user.id, "reply")
        reply1 = update_reply(reply.id, "reply_update")
        assert reply1 is not None

    def test_delete_reply(self):
        reply = create_reply(self.comment.id, self.user.id, "reply")
        delete_reply(reply.id)
        reply1 = get_reply_by_id(reply.id)
        assert reply1 is None


class TestProductQueryIntegration(unittest.TestCase):
    ucount = get_total_user_count()
    user = create_user(f"bob{ucount}", f"bob{ucount}", "bobpass")
    farmer = create_user(
        username=f"rob{ucount}",
        email=f"rob{ucount}@gmail.com",
        password=f"robpass",
        access="farmer",
    )
    pc_count = get_total_category_count()
    pc = create_product_category(f"category{pc_count + 1}")
    pcount = get_total_product_count()
    product = create_product(farmer.id, pc.id, f"product{pcount}", "description", "image.jpg", 10, 10, 10, 10)

    def test_create_query(self):
        query = create_product_query(self.user.id, self.product.id, "query")
        assert query is not None

    def test_get_product_query_by_id(self):
        query = create_product_query(self.user.id, self.product.id, "query")
        query1 = get_product_query_by_id(query.id)
        assert query1 == query

    def test_get_product_query_by_id_json(self):
        query = create_product_query(self.user.id, self.product.id, "query")
        query1 = get_product_query_by_id_json(query.id)
        assert query1 == query.to_json()

    def test_get_product_query_by_product_id(self):
        query = create_product_query(self.user.id, self.product.id, "query")
        query1 = get_product_query_by_product_id(self.product.id)
        assert query in query1

    def test_get_product_query_by_product_id_json(self):
        query = create_product_query(self.user.id, self.product.id, "query")
        query1 = get_product_query_by_product_id_json(self.product.id)
        assert query.to_json() in query1

    def test_get_product_query_by_user_id(self):
        query = create_product_query(self.user.id, self.product.id, "query")
        query1 = get_product_query_by_user_id(self.user.id)
        assert query in query1

    def test_get_product_query_by_user_id_json(self):
        query = create_product_query(self.user.id, self.product.id, "query")
        query1 = get_product_query_by_user_id_json(self.user.id)
        assert query.to_json() in query1

    def test_get_all_product_queries(self):
        query = create_product_query(self.user.id, self.product.id, "query")
        queries = get_all_product_queries()
        assert query in queries

    def test_get_all_product_queries_json(self):
        query = create_product_query(self.user.id, self.product.id, "query")
        queries = get_all_product_queries_json()
        assert query.to_json() in queries

    def test_get_product_queries_by_farmer_id(self):
        query = create_product_query(self.user.id, self.product.id, "query")
        queries = get_product_query_by_farmer_id(self.farmer.id)
        assert query in queries

    def test_get_product_queries_by_farmer_id_json(self):
        query = create_product_query(self.user.id, self.product.id, "query")
        queries = get_product_query_by_farmer_id_json(self.farmer.id)
        assert query.to_json() in queries

    def test_delete_product_query(self):
        query = create_product_query(self.user.id, self.product.id, "query")
        delete_product_query(query.id)
        query1 = get_product_query_by_id(query.id)
        assert query1 is None


class TestProductQueryReplyIntegration(unittest.TestCase):
    ucount = get_total_user_count()
    user = create_user(f"bob{ucount}", f"bob{ucount}", "bobpass")
    farmer = create_user(
        username=f"rob{ucount}",
        email=f"rob{ucount}@gmail.com",
        password=f"robpass",
        access="farmer",
    )
    pc_count = get_total_category_count()
    pc = create_product_category(f"category{pc_count + 1}")
    pcount = get_total_product_count()
    product = create_product(farmer.id, pc.id, f"product{pcount}", "description", "image.jpg", 10, 10, 10, 10)
    query = create_product_query(user.id, product.id, "query")

    def test_create_reply(self):
        reply = create_query_reply(self.query.id, self.farmer.id, "reply")
        assert reply is not None

    def test_get_all_query_replies(self):
        reply = create_query_reply(self.query.id, self.farmer.id, "reply")
        replies = get_all_query_replies()
        assert reply in replies

    def test_get_all_query_replies_by_query_id(self):
        reply = create_query_reply(self.query.id, self.farmer.id, "reply")
        replies = get_all_query_replies_by_query_id(self.query.id)
        assert reply in replies

    def test_get_all_query_replies_by_query_id_json(self):
        reply = create_query_reply(self.query.id, self.farmer.id, "reply")
        replies = get_all_query_replies_by_query_id_json(self.query.id)
        assert reply.to_json() in replies

    def test_get_query_reply_by_id(self):
        reply = create_query_reply(self.query.id, self.farmer.id, "reply")
        reply1 = get_query_reply_by_id(reply.id)
        assert reply1 == reply

    def test_get_query_reply_by_id_json(self):
        reply = create_query_reply(self.query.id, self.farmer.id, "reply")
        reply1 = get_query_reply_by_id_json(reply.id)
        assert reply1 == reply.to_json()

    def test_get_query_replies_by_user_id(self):
        reply = create_query_reply(self.query.id, self.farmer.id, "reply")
        replies = get_query_replies_by_user_id(self.farmer.id)
        assert reply in replies

    def test_get_query_replies_by_user_id_json(self):
        reply = create_query_reply(self.query.id, self.farmer.id, "reply")
        replies = get_query_replies_by_user_id_json(self.farmer.id)
        assert reply.to_json() in replies

    def test_get_query_replies_by_user_name(self):
        reply = create_query_reply(self.query.id, self.farmer.id, "reply")
        replies = get_query_replies_by_user_name(self.farmer.username)
        assert reply in replies

    def test_get_query_replies_by_user_name_json(self):
        reply = create_query_reply(self.query.id, self.farmer.id, "reply")
        replies = get_query_replies_by_user_name_json(self.farmer.username)
        assert reply.to_json() in replies

    def test_update_query_reply(self):
        reply = create_query_reply(self.query.id, self.farmer.id, "reply")
        update_query_reply(reply.id, "reply1")
        reply1 = get_query_reply_by_id(reply.id)
        assert reply1.body == "reply1"

    def test_delete_query_reply(self):
        reply = create_query_reply(self.query.id, self.farmer.id, "reply")
        delete_query_reply(reply.id)
        reply1 = get_query_reply_by_id(reply.id)
        assert reply1 is None


class TestLoggingIntegration(unittest.TestCase):
    ucount = get_total_user_count()
    user = create_user(f"bob{ucount}", f"bob{ucount}", "bobpass")

    def test_create_log(self):
        log = create_log(self.user.id, "log", "log desc")
        assert log is not None

    def test_get_log_by_id(self):
        log = create_log(self.user.id, "log", "log desc")
        log1 = get_log_by_id(log.id)
        assert log1 == log

    def test_get_log_by_id_json(self):
        log = create_log(self.user.id, "log", "log desc")
        log1 = get_log_by_id_json(log.id)
        assert log1 == log.to_json()

    def test_get_logs_by_user_id(self):
        log = create_log(self.user.id, "log", "log desc")
        logs = get_logs_by_user_id(self.user.id)
        assert log in logs

    def test_get_logs_by_user_id_json(self):
        log = create_log(self.user.id, "log", "log desc")
        logs = get_logs_by_user_id_json(self.user.id)
        assert log.to_json() in logs

    def test_get_all_logs(self):
        log = create_log(self.user.id, "log", "log desc")
        logs = get_all_logs()
        assert log in logs

    def test_get_all_logs_json(self):
        log = create_log(self.user.id, "log", "log desc")
        logs = get_all_logs_json()
        assert log.to_json() in logs

    def test_get_logs_by_action(self):
        log = create_log(self.user.id, "log", "log desc")
        logs = get_logs_by_action("log")
        assert log in logs

    def test_get_logs_by_action_json(self):
        log = create_log(self.user.id, "log", "log desc")
        logs = get_logs_by_action_json("log")
        assert log.to_json() in logs

    def test_get_logs_by_user_name(self):
        log = create_log(self.user.id, "log", "log desc")
        logs = get_logs_by_user_name(self.user.username)
        assert log in logs

    def test_get_logs_by_user_name_json(self):
        log = create_log(self.user.id, "log", "log desc")
        logs = get_logs_by_user_name_json(self.user.username)
        assert log.to_json() in logs

    def test_get_all_logs_week(self):
        log = create_log(self.user.id, "log", "log desc")
        logs = get_all_logs_week()
        assert log in logs

    def test_get_all_logs_week_json(self):
        log = create_log(self.user.id, "log", "log desc")
        logs = get_all_logs_week_json()
        assert log.to_json() in logs
