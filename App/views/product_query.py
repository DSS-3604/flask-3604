from flask import Blueprint, jsonify, request

from flask_jwt import jwt_required, current_identity

from App.controllers.product_query import (
    create_product_query,
    get_product_query_by_id,
    get_product_query_by_id_json,
    get_product_query_by_user_id_json,
    get_product_query_by_product_id_json,
    get_product_query_by_farmer_id_json,
    get_all_product_queries_json,
    delete_product_query,
)

from App.controllers.logging import create_log

from App.controllers.user import is_admin

product_query_views = Blueprint("product_query_views", __name__, template_folder="../templates")


@product_query_views.route("/api/product_queries", methods=["GET"])
@jwt_required()
def get_all_product_queries_action():
    if not is_admin(current_identity):
        return (
            jsonify({"message": "You are not authorized to view all product queries"}),
            403,
        )
    product_queries = get_all_product_queries_json()
    if product_queries:
        return (
            jsonify(product_queries.to_json()),
            200,
        )
    return jsonify([]), 200


@product_query_views.route("/api/product_queries/<int:id>", methods=["GET"])
@jwt_required()
def get_product_query_by_id_action(id):
    product_query = get_product_query_by_id_json(id)
    if product_query:
        if (
            not is_admin(current_identity)
            and current_identity.id != product_query.user_id
            and current_identity.id != product_query.farmer_id
        ):
            return jsonify({"message": "You are not authorized to view this product query"}), 403
        return jsonify(product_query), 200
    return jsonify([]), 200


@product_query_views.route("/api/product_queries/user/<int:user_id>", methods=["GET"])
@jwt_required()
def get_product_query_by_user_id_action(user_id):
    if not is_admin(current_identity) and current_identity.id != user_id:
        return jsonify({"message": "You are not authorized to view this product query"}), 403
    product_query = get_product_query_by_user_id_json(user_id)
    if product_query:
        return jsonify(product_query), 200
    return jsonify([]), 200


@product_query_views.route("/api/product_queries/product/<int:product_id>", methods=["GET"])
@jwt_required()
def get_product_query_by_product_id_action(product_id):
    product_query = get_product_query_by_product_id_json(product_id)
    if product_query:
        if not is_admin(current_identity) and current_identity.id != product_query.farmer_id:
            return jsonify({"message": "You are not authorized to view this product query"}), 403
        return jsonify(product_query), 200
    return jsonify([]), 200


@product_query_views.route("/api/product_queries/farmer/<int:farmer_id>", methods=["GET"])
@jwt_required()
def get_product_query_by_farmer_id_action(farmer_id):
    if not is_admin(current_identity) and current_identity.id != farmer_id:
        return jsonify({"message": "You are not authorized to view this product query"}), 403
    product_query = get_product_query_by_farmer_id_json(farmer_id)
    if product_query:
        return jsonify(product_query), 200
    return jsonify([]), 200


@product_query_views.route("/api/product_queries", methods=["POST"])
@jwt_required()
def create_product_query_action():
    data = request.json
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    if not data.get("product_id"):
        return jsonify({"message": "No product id provided"}), 400
    if not data.get("message"):
        return jsonify({"message": "No message provided"}), 400
    product_query = create_product_query(current_identity.id, data.get("product_id"), data.get("message"))
    if product_query:
        create_log(current_identity.id, "Product Query created", f"Product Query {product_query.id} created")
        return jsonify(product_query.to_json()), 201
    return jsonify({"message": "Product Query could not be created"}), 500


@product_query_views.route("/api/product_queries/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_product_query_action(id):
    product_query = get_product_query_by_id(id)
    if product_query:
        if not is_admin(current_identity) and current_identity.id != product_query.user_id:
            return jsonify({"message": "You are not authorized to delete this product query"}), 403
        if delete_product_query(product_query):
            create_log(current_identity.id, "Product Query deleted", f"Product Query {product_query.id} deleted")
            return jsonify({"message": "Product Query deleted"}), 200
        return jsonify({"message": "Product Query could not be deleted"}), 500
    return jsonify({"message": "No product query found"}), 404
