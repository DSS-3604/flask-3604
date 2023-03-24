from flask import Blueprint, jsonify, request

from flask_jwt import jwt_required, current_identity

from App.controllers.product import (
    create_product,
    get_product_by_id,
    update_product,
    delete_product,
    get_all_products_json,
    get_products_by_farmer_id_json,
    get_products_past_week_json,
    get_products_by_category_id_json,
    search_products_by_name_json,
    search_products_by_name_past_week_json,
)

from App.controllers.product_category import (
    get_product_category_by_id,
    get_products_by_category_name_json,
)

from App.controllers.user import is_farmer, is_admin, get_user_by_id

product_views = Blueprint("product_views", __name__, template_folder="../templates")


@product_views.route("/products/farmer/<int:id>", methods=["GET"])
@jwt_required()
def get_farmer_products_action(id):
    farmer = get_user_by_id(id)
    if not farmer:
        return jsonify({"message": "No farmer found"}), 404
    else:
        if not is_farmer(farmer):
            return jsonify({"message": "User is not a farmer"}), 403
    products = get_products_by_farmer_id_json(id)
    if products:
        return jsonify(products), 200
    return jsonify([]), 200


@product_views.route("/products", methods=["GET"])
def get_all_products_action():
    products = get_all_products_json()
    if products:
        return jsonify(products), 200
    return jsonify({"message": "No products found"}), 404


@product_views.route("/products/search/<string:name>", methods=["GET"])
def search_products_action(name):
    products = search_products_by_name_json(name)
    if products:
        return jsonify(products), 200
    return jsonify({"message": "No products found"}), 404


@product_views.route("/products/search/recent/<string:name>", methods=["GET"])
def search_recent_products_action(name):
    products = search_products_by_name_past_week_json(name)
    if products:
        return jsonify(products), 200
    return jsonify({"message": "No recent products found"}), 404


@product_views.route("/products/recent", methods=["GET"])
def get_recent_products_action():
    products = get_products_past_week_json()
    if products:
        return jsonify(products), 200
    return jsonify({"message": "No recent products found"}), 404


@product_views.route("/products", methods=["POST"])
@jwt_required()
def create_product_action():
    data = request.json
    if not is_farmer(current_identity) and not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to create a product"}), 403
    if not get_product_category_by_id(data["category_id"]):
        return jsonify({"message": "No product category found"}), 404
    product = create_product(
        farmer_id=current_identity.id,
        category_id=data["category_id"],
        name=data["name"],
        description=data["description"],
        image=data["image"],
        retail_price=data["retail_price"],
        wholesale_price=data["wholesale_price"],
        wholesale_unit_quantity=data["wholesale_unit_quantity"],
        total_product_quantity=data["total_product_quantity"],
    )
    if product:
        return jsonify(product.to_json()), 201
    return jsonify({"message": "Product creation failed"}), 500


@product_views.route("/products/<int:id>", methods=["GET"])
def get_product_by_id_action(id):
    product = get_product_by_id(id)
    if product:
        return jsonify(product.to_json()), 200
    return jsonify({"message": "No product found"}), 404


# get product by product category
@product_views.route("/products/category/<int:id>", methods=["GET"])
def get_product_by_category_id_action(id):
    products = get_products_by_category_id_json(id)
    if products:
        return jsonify(products), 200
    return jsonify({"message": "No products found"}), 404


# get product by product category name
@product_views.route("/products/category/<string:name>", methods=["GET"])
def get_product_by_category_name_action(name):
    category = get_product_category_by_id(name)
    if category:
        products = get_products_by_category_name_json(name)
        if products:
            return jsonify(products), 200
        return jsonify({"message": "No products found"}), 404
    return jsonify({"message": "No category found"}), 404


@product_views.route("/products/<int:id>", methods=["PUT"])
@jwt_required()
def update_product_action(id):
    data = request.json
    product = get_product_by_id(id)
    if product:
        if not is_farmer(current_identity):
            return (
                jsonify({"message": "You are not authorized to update a product"}),
                403,
            )
        if product.farmer_id != current_identity.id:
            return (
                jsonify({"message": "You are not authorized to update this product"}),
                403,
            )

        if "name" in data:
            product = update_product(id=id, name=data["name"])
        if "description" in data:
            product = update_product(id=id, description=data["description"])
        if "image" in data:
            product = update_product(id=id, image=data["image"])
        if "retail_price" in data:
            product = update_product(id=id, retail_price=data["retail_price"])
        if "wholesale_price" in data:
            product = update_product(id=id, wholesale_price=data["wholesale_price"])
        if "wholesale_unit_quantity" in data:
            product = update_product(
                id=id, wholesale_unit_quantity=data["wholesale_unit_quantity"]
            )
        if "total_product_quantity" in data:
            product = update_product(
                id=id, total_product_quantity=data["total_product_quantity"]
            )
        if "category_id" in data:
            product = update_product(id=id, category_id=data["category_id"])
        return jsonify(product.to_json()), 200
    return jsonify({"message": "No product found"}), 404


@product_views.route("/products/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_product_action(id):
    product = get_product_by_id(id)
    if product:
        if not is_farmer(current_identity) and not is_admin(current_identity):
            return (
                jsonify({"message": "You are not authorized to delete a product"}),
                403,
            )
        if product.farmer_id != current_identity.id and not is_admin(current_identity):
            return (
                jsonify({"message": "You are not authorized to delete this product"}),
                403,
            )
        delete_product(id)
        return jsonify({"message": f"Product {product.name} deleted"}), 200
    return jsonify({"message": "No product found"}), 404
