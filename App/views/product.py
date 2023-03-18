from flask import Blueprint, jsonify, request

from flask_jwt import jwt_required, current_identity

from .index import index_views

from App.controllers.product import (
    create_product,
    get_product_by_id,
    update_product,
    delete_product,
    get_all_products_json,
    get_products_by_farmer_id_json,
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


@product_views.route("/products", methods=["POST"])
@jwt_required()
def create_product_action():
    data = request.json
    if not is_farmer(current_identity):
        return jsonify({"message": "You are not authorized to create a product"}), 403

    create_product(
        farmer_id=current_identity.id,
        name=data["name"],
        description=data["description"],
        image=data["image"],
        retail_price=data["retail_price"],
        wholesale_price=data["wholesale_price"],
        wholesale_unit_quantity=data["wholesale_unit_quantity"],
        total_product_quantity=data["total_product_quantity"],
    )
    return (
        jsonify(
            {
                "message": f"Product {data['name']} created by user: {current_identity.id}"
            }
        ),
        201,
    )


@product_views.route("/products/<int:id>", methods=["GET"])
def get_product_by_id_action(id):
    product = get_product_by_id(id)
    if product:
        return jsonify(product.to_json()), 200
    return jsonify({"message": "No product found"}), 404


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
            update_product(id=id, name=data["name"])
        if "description" in data:
            update_product(id=id, description=data["description"])
        if "image" in data:
            update_product(id=id, image=data["image"])
        if "retail_price" in data:
            update_product(id=id, retail_price=data["retail_price"])
        if "wholesale_price" in data:
            update_product(id=id, wholesale_price=data["wholesale_price"])
        if "wholesale_unit_quantity" in data:
            update_product(
                id=id, wholesale_unit_quantity=data["wholesale_unit_quantity"]
            )
        if "total_product_quantity" in data:
            update_product(id=id, total_product_quantity=data["total_product_quantity"])
        return jsonify({"message": f"Product {id} updated"}), 200
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
