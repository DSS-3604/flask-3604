from flask import Blueprint, jsonify, request

from App.controllers.farmer_review import (
    create_review,
    get_all_reviews_json,
    get_review_by_id,
    get_review_by_id_json,
    get_reviews_by_farmer_id_json,
    get_reviews_by_user_id_json,
    update_review,
    delete_review,
)

from App.controllers.logging import create_log

from App.controllers.user import get_user_by_id, is_admin

from flask_jwt import jwt_required, current_identity

review_views = Blueprint("review_views", __name__, template_folder="../templates")


@review_views.route("/api/farmer/review", methods=["GET"])
@jwt_required()
def get_all_reviews_action():
    reviews = get_all_reviews_json()
    if reviews:
        return jsonify(reviews), 200
    return jsonify([]), 200


@review_views.route("/api/farmer/<int:id>/review", methods=["GET"])
@jwt_required()
def get_all_reviews_by_farmer_id_action(id):
    farmer = get_user_by_id(id)
    if not farmer:
        return jsonify({"message": "No farmer found"}), 404
    reviews = get_reviews_by_farmer_id_json(id)
    if reviews:
        return jsonify(reviews), 200
    return jsonify([]), 200


@review_views.route("/api/farmer/review/user/<int:user_id>", methods=["GET"])
@jwt_required()
def get_all_reviews_by_user_id_action(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "No user found"}), 404
    reviews = get_reviews_by_user_id_json(user_id)
    if reviews:
        return jsonify(reviews), 200
    return jsonify([]), 200


@review_views.route("/api/farmer/review/<int:review_id>", methods=["GET"])
@jwt_required()
def get_review_by_id_action(review_id):
    review = get_review_by_id_json(review_id)
    if review:
        return jsonify(review), 200
    return jsonify([]), 404


@review_views.route("/api/farmer/<int:id>/review", methods=["POST"])
@jwt_required()
def create_review_action(id):
    data = request.json
    farmer = get_user_by_id(id)
    if not farmer:
        return jsonify({"message": "No farmer found"}), 404
    review = create_review(
        farmer_id=id,
        user_id=current_identity.id,
        rating=data["rating"],
        body=data["body"],
    )
    if review:
        create_log(current_identity.id, "Review created", f"Review {review.id} created")
        return jsonify(review.to_json()), 201
    return jsonify({"message": "review not created"}), 400


@review_views.route("/api/farmer/review/<int:review_id>", methods=["PUT"])
@jwt_required()
def update_review_action(review_id):
    data = request.json
    review = get_review_by_id(review_id)
    if review:
        if review.user_id != current_identity.id and not is_admin(current_identity):
            return jsonify({"message": "Not authorized"}), 401
        if "rating" in data and "body" in data:
            review = update_review(review_id, data["rating"], data["body"])
            if review:
                create_log(
                    current_identity.id, "Review updated", f"Review {review.id} updated"
                )
                return jsonify(review.to_json()), 200
            return jsonify({"message": "review not updated"}), 400
        return jsonify({"message": "rating and body required"}), 400
    return jsonify({"message": f"review {review_id} not found"}), 404


@review_views.route("/api/farmer/review/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review_action(review_id):
    review = get_review_by_id(review_id)
    if review:
        if review.user_id != current_identity.id and not is_admin(current_identity):
            return jsonify({"message": "Not authorized"}), 401
        if delete_review(review_id):
            create_log(
                current_identity.id, "Review deleted", f"Review {review.id} deleted"
            )
            return jsonify({"message": f"review {review_id} deleted"}), 200
    return jsonify({"message": f"review {review_id} not found"}), 404
