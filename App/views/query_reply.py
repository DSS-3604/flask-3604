from flask import Blueprint, jsonify, request

from flask_jwt import jwt_required, current_identity

from App.controllers.product_query import get_product_query_by_id_json

from App.controllers.user import is_admin

from App.controllers.logging import create_log

from App.controllers.query_reply import (
    create_query_reply,
    get_all_query_replies_json,
    get_all_query_replies_by_query_id_json,
    get_query_reply_by_id_json,
    get_query_replies_by_user_name_json,
    get_query_replies_by_user_id_json,
    update_query_reply,
    delete_query_reply,
)

query_reply_views = Blueprint("query_reply_views", __name__, template_folder="../templates")


# create a reply
@query_reply_views.route("/api/query/<int:id>/reply", methods=["POST"])
@jwt_required()
def create_query_reply_action(id):
    query = get_product_query_by_id_json(id)
    if not query:
        return jsonify({"message": "No query found"}), 404
    if not is_admin(current_identity) and query["farmer_id"] != current_identity.id:
        return jsonify({"message": "You are not authorized to create a reply to this query"}), 403
    data = request.json
    if not data["body"]:
        return jsonify({"message": "Body is required"}), 400
    reply = create_query_reply(query_id=id, user_id=current_identity.id, body=data["body"])
    if reply:
        create_log(current_identity.id, "Query reply created", f"Query reply {reply.id} created")
        return jsonify(reply.to_json()), 201
    return jsonify({"message": "Could not create query reply"}), 500


# update a reply
@query_reply_views.route("/api/query/reply/<int:id>", methods=["PUT"])
@jwt_required()
def update_query_reply_action(id):
    reply = get_query_reply_by_id_json(id)
    if not is_admin(current_identity) and reply["user_id"] != current_identity.id:
        return jsonify({"message": "You are not authorized to update this query reply"}), 403
    data = request.json
    if not data["body"]:
        return jsonify({"message": "Body is required"}), 400
    reply = update_query_reply(id, data["body"])
    if reply:
        create_log(current_identity.id, "Query reply updated", f"Query reply {reply.id} updated")
        return jsonify(reply.to_json()), 200
    return jsonify({"message": "Could not update query reply"}), 500


# delete a reply
@query_reply_views.route("/api/query/reply/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_query_reply_action(id):
    reply = get_query_reply_by_id_json(id)
    if not is_admin(current_identity) and reply["user_id"] != current_identity.id:
        return jsonify({"message": "You are not authorized to delete this query reply"}), 403
    if not reply:
        return jsonify({"message": "No query reply found"}), 404
    reply = delete_query_reply(id)
    if reply:
        create_log(current_identity.id, "Query reply deleted", f"Query reply {reply.id} deleted")
        return jsonify(reply.to_json()), 200
    return jsonify({"message": "Could not delete query reply"}), 500


# get all replies by query id
@query_reply_views.route("/api/query/<int:id>/replies", methods=["GET"])
@jwt_required()
def get_all_query_replies_by_query_id_action(id):
    query = get_product_query_by_id_json(id)
    if not query:
        return jsonify({"message": "No query found"}), 404
    if (
        not is_admin(current_identity)
        and query["user_id"] != current_identity.id
        and query["farmer_id"] != current_identity.id
    ):
        return jsonify({"message": "You are not authorized to view this query replies"}), 403
    replies = get_all_query_replies_by_query_id_json(id)
    if replies:
        return jsonify(replies), 200
    return jsonify([]), 200


# get a reply by query reply id
@query_reply_views.route("/api/query/reply/<int:id>", methods=["GET"])
@jwt_required()
def get_query_reply_by_id_action(id):
    reply = get_query_reply_by_id_json(id)
    query = get_product_query_by_id_json(reply["query_id"])
    if (
        not is_admin(current_identity)
        and query["user_id"] != current_identity.id
        and query["farmer_id"] != current_identity.id
    ):
        return jsonify({"message": "You are not authorized to view this query reply"}), 403
    if reply:
        return jsonify(reply), 200
    return jsonify([]), 200


# get all replies by user id
@query_reply_views.route("/api/query/replies/user/<int:id>", methods=["GET"])
@jwt_required()
def get_query_replies_by_user_id_action(id):
    replies = get_query_replies_by_user_id_json(id)
    if not is_admin(current_identity) and current_identity.id != id:
        return jsonify({"message": "You are not authorized to view this query replies"}), 403
    if replies:
        return jsonify(replies), 200
    return jsonify([]), 200


# get all replies by username
@query_reply_views.route("/api/query/replies/user/<string:name>", methods=["GET"])
@jwt_required()
def get_query_replies_by_user_name_action(name):
    replies = get_query_replies_by_user_name_json(name)
    if not is_admin(current_identity) and current_identity.username != name:
        return jsonify({"message": "You are not authorized to view this query replies"}), 403
    if replies:
        return jsonify(replies), 200
    return jsonify([]), 200


# get query replies
@query_reply_views.route("/api/query/replies", methods=["GET"])
@jwt_required()
def get_query_replies_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view this query replies"}), 403
    replies = get_all_query_replies_json()
    if replies:
        return jsonify(replies), 200
    return jsonify([]), 200
