from App.controllers.user import create_user, create_admin, get_user_by_username
from App.controllers.farmer_application import create_farmer_application, approve_farmer_application
from App.controllers.product import create_product
from App.controllers.product_category import create_product_category
import random


# create 10 dummy regular users
def create_dummy_users():
    for i in range(10):
        create_user(
            username="user" + str(i),
            email="user" + str(i) + "@gmail.com",
            password="password",
            access="user",
            bio="",
            phone="",
            address="",
            currency="USD",
            units="kg",
            avatar="",
        )


# create 2 dummy admin users
def create_dummy_admins():
    for i in range(2):
        create_admin(
            username="admin" + str(i),
            email="admin" + str(i) + "@gmail.com",
            password="password",
        )


# create two users and farmer applications, then approve both
def create_dummy_farmers():
    user1 = create_user(
        username="farmer1",
        email="farmer1@gmail.com",
        password="password",
        access="user",
        bio="",
        phone="",
        address="",
        currency="USD",
        units="kg",
        avatar="",
    )
    user2 = create_user(
        username="farmer2",
        email="farmer2@gmail.com",
        password="password",
        access="user",
        bio="",
        phone="",
        address="",
        currency="USD",
        units="kg",
        avatar="",
    )
    app1 = create_farmer_application(user1.id, "farm1")
    app2 = create_farmer_application(user2.id, "farm2")
    approve_farmer_application(app1.id)
    approve_farmer_application(app2.id)
    # create dummy product categories
    create_product_category("category1")
    create_product_category("category2")
    create_product_category("category3")

    # create 10 products for each farmer with random wholesale and retails prices between 20 and 100 and total quantities between 100 and 1000
    for i in range(10):
        create_product(
            farmer_id=user1.id,
            category_id=i % 3 + 1,
            name="product" + str(i),
            description="",
            retail_price=random.randint(20, 100),
            wholesale_price=random.randint(20, 100),
            wholesale_unit_quantity=random.randint(1, 10),
            total_product_quantity=random.randint(100, 1000),
        )
        create_product(
            farmer_id=user2.id,
            category_id=i % 3 + 1,
            name="product" + str(i + 10),
            description="",
            retail_price=random.randint(20, 100),
            wholesale_price=random.randint(20, 100),
            wholesale_unit_quantity=random.randint(1, 10),
            total_product_quantity=random.randint(100, 1000),
        )


# create dummy data
def create_dummy_data():
    user = get_user_by_username("user0")
    if user is None:
        create_dummy_users()
        create_dummy_admins()
        create_dummy_farmers()
        return True
    return False
