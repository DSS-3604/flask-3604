from flask import Blueprint, jsonify, request

from flask_jwt import jwt_required, current_identity

from .index import index_views

from App.controllers.review import (
    create_review,
    get_all_reviews,
    get_all_reviews_json,
    get_review_by_id,
    get_review_by_id_json,
    get_reviews_by_product_id,
    get_reviews_by_product_id_json,
    get_reviews_by_user_id,
    get_reviews_by_user_id_json,
    update_review,
    delete_review,
)

from App.controllers.user import is_farmer, is_admin

review_views = Blueprint("review_views", __name__, template_folder="../templates")

@review_views.route("/review", methods=["GET"])
def get_all_reviews_action():
    reviews = get_all_reviews_json()
    if reviews:
        return jsonify(reviews), 200
    return jsonify({"message": "No products found"}), 404

@review_views.route("/review", methods=["POST"])
def create_review_action():
    data = request.json

    create_review(     
        product_id=data["product_id"], 
        user_id=data["user_id"], 
        body=data["body"]
    )
    return jsonify({"message": f"Review {data['product_id']} created"}), 201

@review_views.route("/review/<int:id>", methods=["PUT"])
def update_review_action(id):
    data = request.json
    review = get_review_by_id(id)
    if review:
        if 'body' in data:
            update_review(id=id, body=data['body'])
        return jsonify({"message": f"Review {id} updated"}), 200
    return jsonify({"message": "No review found"}), 404

@review_views.route("/review/<int:id>", methods=["DELETE"])
def delete_review_action(id):
    review = get_review_by_id(id)
    if review:
        delete_review(id)
        return jsonify({"message": f"Review {id} deleted"}), 200
    return jsonify({"message": "No review found"}), 404

