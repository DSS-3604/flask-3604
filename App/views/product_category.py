from flask import Blueprint, jsonify, request

from flask_jwt import jwt_required, current_identity

from App.controllers.product_category import (
    create_product_category,
    get_product_category_by_id_json,
    update_product_category,
    delete_product_category,
    get_product_category_by_name_json,
    get_product_categories_json,
)

from App.controllers.user import is_admin


product_category_views = Blueprint(
    "product_category_views", __name__, template_folder="../templates"
)


@product_category_views.route("/product_categories", methods=["GET"])
def get_all_product_categories_action():
    product_categories = get_product_categories_json()
    if product_categories:
        return jsonify(product_categories), 200
    return jsonify({"message": "No product categories found"}), 404


# get product category by id
@product_category_views.route("/product_categories/<int:id>", methods=["GET"])
def get_product_category_by_id_action(id):
    product_category = get_product_category_by_id_json(id)
    if product_category:
        return jsonify(product_category), 200
    return jsonify({"message": "No product category found"}), 404


# get product category by name
@product_category_views.route("/product_categories/<string:name>", methods=["GET"])
def get_product_category_by_name_action(name):
    product_category = get_product_category_by_name_json(name)
    if product_category:
        return jsonify(product_category), 200
    return jsonify({"message": "No product category found"}), 404


# create product category
@product_category_views.route("/product_categories", methods=["POST"])
@jwt_required()
def create_product_category_action():
    data = request.json
    if not is_admin(current_identity):
        return (
            jsonify({"message": "You are not authorized to create a product category"}),
            403,
        )

    if not data["name"]:
        return jsonify({"message": "Name is required"}), 400

    pc = create_product_category(name=data["name"])
    if pc:
        return jsonify(pc.to_json()), 201
    return jsonify({"message": "Product category could not be created"}), 400


# update product category
@product_category_views.route("/product_categories/<int:id>", methods=["PUT"])
@jwt_required()
def update_product_category_action(id):
    data = request.json
    if not is_admin(current_identity):
        return (
            jsonify({"message": "You are not authorized to update a product category"}),
            403,
        )

    if not data["name"]:
        return jsonify({"message": "Name is required"}), 400
    pc = update_product_category(id, name=data["name"])
    if pc:
        return jsonify(pc.to_json()), 200
    return jsonify({"message": f"Product category {id} does not exist"}), 404


# delete product category
@product_category_views.route("/product_categories/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_product_category_action(id):
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to delete a product "}), 403
    if delete_product_category(id):
        return jsonify({"message": f"Product category {id} deleted"}), 200
    return (
        jsonify(
            {"message": f"Product category {id} does not exist or could not be deleted"}
        ),
        404,
    )
