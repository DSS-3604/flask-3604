from flask import Blueprint, jsonify, request

from flask_jwt import jwt_required, current_identity

from .index import index_views

from App.controllers.reply import (
    create_reply,
    get_all_replies_by_review_id,
    get_all_replies_by_review_id_json,
    get_reply_by_id,
    get_reply_by_id_json,
    get_replies_by_user_id,
    get_replies_by_user_id_json,
    update_reply,
    delete_reply,
)

reply_views = Blueprint("reply_views", __name__, template_folder="../templates")


@reply_views.route("/product/review/replies", methods=["GET"])
@jwt_required()
def get_all_replies_action():
    replies = get_all_replies_by_review_id_json()
    if replies:
        return jsonify(replies), 200
    return jsonify([]), 200


@reply_views.route("/product/review/reply", methods=["POST"])
@jwt_required()
def create_reply_action():
    data = request.json
    create_reply(
        review_id=data["review_id"],
        user_id=data["user_id"],
        body=data["body"]
    )
    return jsonify({"message": f"Reply {data['review_id']} created"}), 201


@reply_views.route("/product/review/reply/<int:id>", methods=["PUT"])
@jwt_required()
def update_reply_action(id):
    data = request.json
    reply = get_reply_by_id(id)
    if reply:
        if 'body' in data:
            update_reply(id=id, body=data['body'])
        return jsonify({"message": f"Reply {id} updated"}), 200
    return jsonify({"message": "No reply found"}), 404


@reply_views.route("/product/review/reply/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_reply_action(id):
    reply = get_reply_by_id(id)
    if reply:
        delete_reply(id)
        return jsonify({"message": f"Reply {id} deleted"}), 200
    return jsonify({"message": "No reply found"}), 404
