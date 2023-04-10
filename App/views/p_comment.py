from flask import Blueprint, jsonify, request

from App.controllers.p_comment import (
    create_comment,
    get_all_comments_json,
    get_comment_by_id,
    get_comment_by_id_json,
    update_comment,
    delete_comment,
)

from App.controllers.logging import create_log

from App.controllers.product import get_product_by_id

from flask_jwt import jwt_required, current_identity

comment_views = Blueprint("comment_views", __name__, template_folder="../templates")


@comment_views.route("/api/product/comment", methods=["GET"])
@jwt_required()
def get_all_comments_action():
    comments = get_all_comments_json()
    if comments:
        return jsonify(comments), 200
    return jsonify([]), 200


@comment_views.route("/api/product/comment/<int:id>", methods=["GET"])
@jwt_required()
def get_comment_by_id_action(id):
    comment = get_comment_by_id_json(id)
    if comment:
        return jsonify(comment), 200
    return jsonify([]), 404


@comment_views.route("/api/product/comment", methods=["POST"])
@jwt_required()
def create_comment_action():
    data = request.json
    if "product_id" in data:
        product = get_product_by_id(data["product_id"])
        if not product:
            return jsonify({"message": "No product found"}), 404
    comment = create_comment(product_id=data["product_id"], user_id=current_identity.id, body=data["body"])
    if comment:
        create_log(current_identity.id, "Comment created", f"Comment {comment.id} created")
        return jsonify(comment.to_json()), 201
    return jsonify({"message": "Could not create comment"}), 400


@comment_views.route("/api/product/comment/<int:id>", methods=["PUT"])
@jwt_required()
def update_comment_action(id):
    data = request.json
    comment = get_comment_by_id(id)
    if comment:
        if current_identity.id != comment.user_id and not current_identity.is_admin:
            return (
                jsonify({"message": "You are not allowed to update this comment"}),
                403,
            )
        if "body" in data:
            comment = update_comment(id=id, body=data["body"])
            if comment:
                create_log(
                    current_identity.id,
                    "Comment updated",
                    f"Comment {comment.id} updated",
                )
                return jsonify(comment.to_json()), 200
            return jsonify({"message": "Could not update comment"}), 400
        else:
            return jsonify({"message": "No data to update"}), 400
    return jsonify({"message": "No comment found"}), 404


@comment_views.route("/api/product/comment/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_comment_action(id):
    comment = get_comment_by_id(id)
    if comment:
        if current_identity.id != comment.user_id and not current_identity.is_admin:
            return (
                jsonify({"message": "You are not allowed to delete this comment"}),
                403,
            )

        if delete_comment(id):
            create_log(current_identity.id, "Comment deleted", f"Comment {comment.id} deleted")
            return jsonify({"message": f"comment {id} deleted"}), 200
    return jsonify({"message": "No comment found"}), 404
