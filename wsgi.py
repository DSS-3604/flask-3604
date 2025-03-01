import click
import pytest
import sys
from flask.cli import AppGroup

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

from App.controllers.p_comment import (
    create_comment,
    get_all_comments,
    get_all_comments_json,
    get_comments_by_product_id,
    get_comments_by_product_id_json,
)
from App.controllers.product import (
    create_product,
    get_all_products,
    get_all_products_json,
    update_product,
    delete_product,
    search_products_by_name_json,
)

from App.controllers.product_category import create_product_category

from App.controllers.p_reply import (
    create_reply,
)

from App.controllers.farmer_review import (
    create_review,
)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


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


@product_cli.command("create-category", help="Creates a product category")
@click.argument("name", default="tomato")
def create_product_category_command(name):
    product_category = create_product_category(name)
    print(product_category.to_json())


app.cli.add_command(product_cli)

comment_cli = AppGroup("comment", help="comment object commands")


@comment_cli.command("create", help="Creates a comment")
@click.argument("product_id", default=1)
@click.argument("user_id", default=1)
@click.argument("body", default="body")
def create_comment_command(product_id, user_id, body):
    comment = create_comment(product_id, user_id, body)
    print(comment.to_json())


@comment_cli.command("reply", help="Replies to a comment")
@click.argument("comment_id", default=1)
@click.argument("user_id", default=2)
@click.argument("body", default="body")
def reply_comment_command(comment_id, user_id, body):
    comment = create_reply(comment_id, user_id, body)
    print(comment.to_json())


@comment_cli.command("list", help="Lists comments in the database")
@click.argument("format", default="string")
def list_comment_command(format):
    if format == "string":
        print(get_all_comments())
    else:
        print(get_all_comments_json())


@comment_cli.command("list-by-product", help="Lists comments by product in the database")
@click.argument("product_id", default=1)
@click.argument("format", default="string")
def list_comment_by_product_command(product_id, format):
    if format == "string":
        print(get_comments_by_product_id(product_id))
    else:
        print(get_comments_by_product_id_json(product_id))


app.cli.add_command(comment_cli)

"""
Generic Commands
"""


@app.cli.command("init")
def initialize():
    create_db(app)
    print("database initialized")


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
    user1 = create_user(
        "bob",
        "bob@gmail.com",
        "bobpass",
        "user",
        "bob is a user",
        "800-1234",
        "University Drive",
    )
    user2 = create_user("farmerguy1", "farmerguy1@gmail.com", "farmerguy1", "user")
    user3 = create_user("farmerguy321", "farmerguy321@gmail.com", "farmerguy321", "user")
    print(f"admin1: {admin1.to_json()}")
    print(f"user1: {user1.to_json()}")
    f_application = create_farmer_application(user2.id, "i wanna be a farmer")
    print(f"farmer_application: {f_application.to_json()}")
    f_application2 = create_farmer_application(user3.id, "i wanna be a farmer")
    print(f"farmer_application2: {f_application2.to_json()}")
    reject_farmer_application(f_application.id)
    print(f"farmer_application: {f_application.to_json()}")
    approve_farmer_application(f_application2.id)
    print(f"farmer_application2: {f_application2.to_json()}")

    category1 = create_product_category("tomato")
    category2 = create_product_category("potato")
    category3 = create_product_category("carrot")
    category4 = create_product_category("onion")

    product1 = create_product(
        farmer_id=user3.id,
        category_id=category1.id,
        name="cherry tomato",
        description="red",
        retail_price=1,
        wholesale_price=1,
        wholesale_unit_quantity=1,
        total_product_quantity=1,
    )
    product2 = create_product(
        farmer_id=user3.id,
        category_id=category2.id,
        name="idaho potato",
        description="brown",
        retail_price=1,
        wholesale_price=1,
        wholesale_unit_quantity=1,
        total_product_quantity=1,
    )
    product3 = create_product(
        farmer_id=user3.id,
        category_id=category3.id,
        name="baby carrot",
        description="orange",
        retail_price=1,
        wholesale_price=1,
        wholesale_unit_quantity=1,
        total_product_quantity=1,
    )
    product4 = create_product(
        farmer_id=user3.id,
        category_id=category4.id,
        name="scorpion pepper",
        description="red",
        retail_price=1,
        wholesale_price=1,
        wholesale_unit_quantity=1,
        total_product_quantity=1,
    )
    print(f"product1: {product1.to_json()}")
    print(f"product2: {product2.to_json()}")
    print(f"product3: {product3.to_json()}")
    print(f"product4: {product4.to_json()}")

    comment1 = create_comment(product1.id, user1.id, "bad")

    comment2 = create_comment(product1.id, admin1.id, "ok")

    comment3 = create_comment(product1.id, user3.id, "good")

    create_reply(comment1.id, admin1.id, "reply1")
    create_reply(comment2.id, admin1.id, "reply2")
    create_reply(comment3.id, admin1.id, "reply3")
    create_reply(comment1.id, user3.id, "reply4")
    create_reply(comment2.id, user3.id, "reply5")
    create_reply(comment3.id, user3.id, "reply6")
    create_reply(comment1.id, user1.id, "reply7")
    create_reply(comment2.id, user1.id, "reply8")
    create_reply(comment3.id, user1.id, "reply9")
    print(f"comment1: {comment1.to_json()}")
    # print(get_all_replies_by_comment_id(comment1.id))))
    print(f"comment2: {comment2.to_json()}")
    # print(get_all_replies_by_comment_id(comment2.id)
    print(f"comment3: {comment3.to_json()}")
    # print(get_all_replies_by_comment_id(comment3.id)

    review1 = create_review(user3.id, user1.id, 5, "great service")
    review2 = create_review(user3.id, admin1.id, 4, "good service")
    review3 = create_review(user3.id, user1.id, 1, "horrible service")
    print(f"review1: {review1.to_json()}")
    print(f"review2: {review2.to_json()}")
    print(f"review3: {review3.to_json()}")


# get all products then
# replace all product images with "https://s3.eu-west-2.amazonaws.com/devo.core.images/products/b1bf55b2-18c6-4184-9522-72b28b13d62d_5054073003722.png"
@test.command("images", help="Replace all product images with a default image")
def replace_all_product_images_command():
    products = get_all_products()
    for product in products:
        update_product(
            id=product.id,
            image="https://s3.eu-west-2.amazonaws.com/devo.core.images/products/b1bf55b2-18c6-4184-9522-72b28b13d62d_5054073003722.png",
        )
    print("All product images replaced with default image")


@test.command("product", help="Search for products")
@click.argument("name")
def product_search_command(name):
    products = search_products_by_name_json(name)
    print(products)


app.cli.add_command(test)
