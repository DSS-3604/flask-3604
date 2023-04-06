from flask import Blueprint, jsonify, request

from flask_jwt import jwt_required, current_identity

from App.controllers.p_comment import get_comment_by_id

from App.controllers.user import is_admin

from App.controllers.p_reply import (
    create_reply,
    get_all_replies_by_comment_id_json,
    get_reply_by_id,
    get_reply_by_id_json,
    update_reply,
    delete_reply,
)

from App.controllers.logging import create_log

reply_views = Blueprint("reply_views", __name__, template_folder="../templates")


@reply_views.route("/product/comment/<int:id>/reply", methods=["GET"])
@jwt_required()
def get_all_replies_by_comment_id_action(id):
    replies = get_all_replies_by_comment_id_json(id)
    if replies:
        return jsonify(replies), 200
    return jsonify([]), 200


@reply_views.route("/product/comment/reply/<int:id>", methods=["GET"])
@jwt_required()
def get_reply_by_id_action(id):
    reply = get_reply_by_id_json(id)
    if reply:
        return jsonify(reply), 200
    return jsonify({}), 404


@reply_views.route("/product/comment/<int:id>/reply", methods=["POST"])
@jwt_required()
def create_reply_action(id):
    comment = get_comment_by_id(id)
    if not comment:
        return jsonify({"message": "No comment found"}), 404
    data = request.json
    reply = create_reply(comment_id=id, user_id=current_identity.id, body=data["body"])
    if reply:
        create_log(current_identity.id, "Reply created", f"Reply {reply.id} created")
        return jsonify(reply.to_json()), 201
    return jsonify({"message": "Could not create reply"}), 500


@reply_views.route("/product/comment/reply/<int:id>", methods=["PUT"])
@jwt_required()
def update_reply_action(id):
    data = request.json
    reply = get_reply_by_id(id)
    if reply:
        if not reply.user_id == current_identity.id and not is_admin(current_identity):
            return jsonify({"message": "Not authorized"}), 401
        if "body" in data:
            reply = update_reply(reply_id=id, body=data["body"])
            if reply:
                create_log(current_identity.id, "Reply updated", f"Reply {reply.id} updated")
                return jsonify(reply), 200
            return jsonify({"message": "Could not update reply"}), 500
        return jsonify({"message": "No body found"}), 400
    return jsonify({"message": "No reply found"}), 404


@reply_views.route("/product/comment/reply/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_reply_action(id):
    reply = get_reply_by_id(id)
    if reply:
        if not reply.user_id == current_identity.id and not is_admin(current_identity):
            return jsonify({"message": "Not authorized"}), 401
        if delete_reply(id):
            create_log(current_identity.id, "Reply deleted", f"Reply {id} deleted")
            return jsonify({"message": f"Reply {id} deleted"}), 200
    return jsonify({"message": "No reply found"}), 404
