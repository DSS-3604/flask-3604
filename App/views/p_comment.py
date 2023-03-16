from flask import Blueprint, jsonify, request

from .index import index_views

from App.controllers.p_comment import (
    create_comment,
    get_all_comments,
    get_all_comments_json,
    get_comment_by_id,
    get_comment_by_id_json,
    get_comments_by_product_id,
    get_comments_by_product_id_json,
    get_comments_by_user_id,
    get_comments_by_user_id_json,
    update_comment,
    delete_comment,
)
from flask_jwt import jwt_required, current_identity

comment_views = Blueprint("comment_views", __name__, template_folder="../templates")


@comment_views.route("/product/comments", methods=["GET"])
@jwt_required()
def get_all_comments_action():
    comments = get_all_comments_json()
    if comments:
        return jsonify(comments), 200
    return jsonify([]), 200


@comment_views.route("/product/comment", methods=["POST"])
@jwt_required()
def create_comment_action():
    data = request.json
    create_comment(
        product_id=data["product_id"],
        user_id=data["user_id"],
        body=data["body"]
    )
    return jsonify({"message": f"comment {data['product_id']} created"}), 201


@comment_views.route("/product/comment/<int:id>", methods=["PUT"])
@jwt_required()
def update_comment_action(id):
    data = request.json
    comment = get_comment_by_id(id)
    if comment:
        if 'body' in data:
            update_comment(id=id, body=data['body'])
        return jsonify({"message": f"comment {id} updated"}), 200
    return jsonify({"message": "No comment found"}), 404


@comment_views.route("/product/comment/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_comment_action(id):
    comment = get_comment_by_id(id)
    if comment:
        delete_comment(id)
        return jsonify({"message": f"comment {id} deleted"}), 200
    return jsonify({"message": "No comment found"}), 404
