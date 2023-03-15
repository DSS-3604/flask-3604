import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import create_db, get_migrate
from App.main import create_app

from App.controllers.user import (
    create_user,
    create_admin,
    get_all_users,
    get_all_users_json,
)

from App.controllers.farmer_application import (
    create_farmer_application,
    approve_farmer_application,
    reject_farmer_application,
)

from App.controllers.review import (
    create_review,
    get_all_reviews,
    get_all_reviews_json,
    get_reviews_by_product_id,
    get_reviews_by_product_id_json,
)
from App.controllers.product import (
    create_product,
    get_all_products,
    get_all_products_json,
    update_product,
    delete_product,
)

from App.controllers.reply import (
    create_reply,
)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    create_db(app)
    print("database intialized")


"""
User Commands
"""

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup("user", help="User object commands")


# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create-user", help="Creates a user")
@click.argument("username", default="bob")
@click.argument("email", default="bob@bobmail.com")
@click.argument("password", default="bobpass")
def create_user_command(username, email, password):
    user = create_user(username, email, password, "user")
    print(user.to_json())


@user_cli.command("create-farmer", help="Creates a farmer")
@click.argument("username", default="farmerbob")
@click.argument("email", default="farmerbob@bobmail.com")
@click.argument("password", default="bobpass")
def create_farmer_command(username, email, password):
    user = create_user(username, email, password, "farmer")
    print(user.to_json())


@user_cli.command("create-admin", help="Creates an admin")
@click.argument("username", default="adminbob")
@click.argument("email", default="adminbob@bobmail.com")
@click.argument("password", default="bobpass")
def create_admin_command(username, email, password):
    user = create_user(username, email, password, "admin")
    print(user.to_json())


# this command will be : flask user create bob bobpass


@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == "string":
        print(get_all_users())
    else:
        print(get_all_users_json())


app.cli.add_command(user_cli)  # add the group to the cli


product_cli = AppGroup("product", help="Product object commands")


@product_cli.command("create", help="Creates a product")
@click.argument("name", default="tomato")
@click.argument("description", default="red")
@click.argument("image", default="image")
@click.argument("price", default=1)
@click.argument("quantity", default=1)
@click.argument("farmer_id", default=2)
def create_product_command(name, description, image, price, quantity, farmer_id):
    product = create_product(name, description, image, price, quantity, farmer_id)
    print(product.to_json())


@product_cli.command("list", help="Lists products in the database")
@click.argument("format", default="string")
def list_product_command(format):
    if format == "string":
        print(get_all_products())
    else:
        print(get_all_products_json())


@product_cli.command("update", help="Updates a product")
@click.argument("id", default=1)
@click.argument("name", default="tomato")
@click.argument("description", default="green")
@click.argument("image", default="image")
@click.argument("price", default=1)
@click.argument("quantity", default=1)
def update_product_command(id, name, description, image, price, quantity):
    update_product(id, name, description, image, price, quantity)
    print(f"{id} updated!")


@product_cli.command("delete", help="Deletes a product")
@click.argument("id", default=1)
def delete_product_command(id):
    delete_product(id)
    print(f"{id} deleted!")


app.cli.add_command(product_cli)

review_cli = AppGroup("review", help="Review object commands")


@review_cli.command("create", help="Creates a review")
@click.argument("product_id", default=1)
@click.argument("user_id", default=1)
@click.argument("rating", default=1)
@click.argument("body", default="body")
def create_review_command(product_id, user_id, rating, body):
    review = create_review(product_id, user_id, rating, body)
    print(review.to_json())


@review_cli.command("reply", help="Replies to a review")
@click.argument("review_id", default=1)
@click.argument("user_id", default=2)
@click.argument("body", default="body")
def reply_review_command(review_id, user_id, body):
    review = create_reply(review_id, user_id, body)
    print(review.to_json())


@review_cli.command("list", help="Lists reviews in the database")
@click.argument("format", default="string")
def list_review_command(format):
    if format == "string":
        print(get_all_reviews())
    else:
        print(get_all_reviews_json())


@review_cli.command("list-by-product", help="Lists reviews by product in the database")
@click.argument("product_id", default=1)
@click.argument("format", default="string")
def list_review_by_product_command(product_id, format):
    if format == "string":
        print(get_reviews_by_product_id(product_id))
    else:
        print(get_reviews_by_product_id_json(product_id))


app.cli.add_command(review_cli)


"""
Generic Commands
"""


@app.cli.command("init")
def initialize():
    create_db(app)
    print("database intialized")


@app.cli.command("run")
def initialize():
    print("hello")


"""
Test Commands
"""

test = AppGroup("test", help="Testing commands")


@test.command("demo", help="Run Demo tests")
def demo_tests_command():
    admin1 = create_admin("admin", "admin@gmail.com", "adminpass")
    user1 = create_user("bob", "bob@gmail.com", "bobpass", "user", "bob is a user", "800-1234", "University Drive")
    print(f"admin1: {admin1.to_json()}")
    print(f"user1: {user1.to_json()}")
    f_application = create_farmer_application("farmer1", "farmer@gmail.com", "i want to be a farmer", "800-1234",
                                              "University Drive")
    print(f"farmer_application: {f_application.to_json()}")
    f_application2 = create_farmer_application("farmer2", "farmer2@gmail.com", "i want to be a farmer", "800-4321",
                                               "University Drive")
    print(f"farmer_application2: {f_application2.to_json()}")
    reject_farmer_application(f_application.id)
    print(f"farmer_application: {f_application.to_json()}")
    farmer = approve_farmer_application(f_application2.id)
    print(f"farmer_application2: {f_application2.to_json()}")

    product1 = create_product("tomato", "red", "image", 1, 1, farmer.id)
    print(f"product1: {product1.to_json()}")
    product2 = create_product("tomato", "green", "image", 1, 1, farmer.id)
    print(f"product2: {product2.to_json()}")
    product3 = create_product("tomato", "yellow", "image", 1, 1, farmer.id)
    print(f"product3: {product3.to_json()}")
    product4 = create_product("tomato", "blue", "image", 1, 1, farmer.id)
    print(f"product4: {product4.to_json()}")

    review1 = create_review(product1.id, user1.id, 1, "bad")
    print(f"review1: {review1.to_json()}")
    review2 = create_review(product1.id, admin1.id, 2, "ok")
    print(f"review2: {review2.to_json()}")
    review3 = create_review(product1.id, farmer.id, 3, "good")
    print(f"review3: {review3.to_json()}")

    create_reply(review1.id, admin1.id, "reply1")
    create_reply(review2.id, admin1.id, "reply2")
    create_reply(review3.id, admin1.id, "reply3")
    create_reply(review1.id, farmer.id, "reply4")
    create_reply(review2.id, farmer.id, "reply5")
    create_reply(review3.id, farmer.id, "reply6")
    create_reply(review1.id, user1.id, "reply7")
    create_reply(review2.id, user1.id, "reply8")
    create_reply(review3.id, user1.id, "reply9")


@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


app.cli.add_command(test)
