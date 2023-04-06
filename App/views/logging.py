from flask import Blueprint, jsonify, request

from App.controllers.logging import (
    get_all_logs_json,
    get_all_logs_week_json,
    get_log_by_id_json,
    get_logs_by_action_json,
    get_logs_by_user_id_json,
    get_logs_by_user_name_json,
)

from App.controllers.user import get_user_by_id, is_admin

from flask_jwt import jwt_required, current_identity

logging_views = Blueprint("logging_views", __name__, template_folder="../templates")


@logging_views.route("/logs", methods=["GET"])
@jwt_required()
def get_all_logs_action():
    if not is_admin(current_identity):
        return jsonify({"message": "User is not an admin"}), 403
    logs = get_all_logs_json()
    if logs:
        return jsonify(logs), 200
    return jsonify([]), 200


# get all logs past week
@logging_views.route("/logs/week", methods=["GET"])
@jwt_required()
def get_all_logs_week_action():
    if not is_admin(current_identity):
        return jsonify({"message": "User is not an admin"}), 403
    logs = get_all_logs_week_json()
    if logs:
        return jsonify(logs), 200
    return jsonify([]), 200


@logging_views.route("/logs/<int:id>", methods=["GET"])
@jwt_required()
def get_log_by_id_action(id):
    if not is_admin(current_identity):
        return jsonify({"message": "User is not an admin"}), 403
    log = get_log_by_id_json(id)
    if log:
        return jsonify(log), 200
    return jsonify({"message": "No log found"}), 404


@logging_views.route("/logs/user/<int:user_id>", methods=["GET"])
@jwt_required()
def get_logs_by_user_id_action(user_id):
    if not is_admin(current_identity):
        return jsonify({"message": "User is not an admin"}), 403
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "No user found"}), 404
    logs = get_logs_by_user_id_json(user_id)
    if logs:
        return jsonify(logs), 200
    return jsonify([]), 200


@logging_views.route("/logs/user/<string:user_name>", methods=["GET"])
@jwt_required()
def get_logs_by_user_name_action(user_name):
    if not is_admin(current_identity):
        return jsonify({"message": "User is not an admin"}), 403
    logs = get_logs_by_user_name_json(user_name)
    if logs:
        return jsonify(logs), 200
    return jsonify([]), 200


@logging_views.route("/logs/action", methods=["GET"])
@jwt_required()
def get_logs_by_action_action():
    if not is_admin(current_identity):
        return jsonify({"message": "User is not an admin"}), 403
    data = request.json
    logs = get_logs_by_action_json(data["action"])
    if logs:
        return jsonify(logs), 200
    return jsonify([]), 200
