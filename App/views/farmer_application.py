from flask import Blueprint, jsonify, request

from flask_jwt import jwt_required, current_identity

from datetime import datetime, timedelta

from App.controllers.farmer_application import (
    create_farmer_application,
    get_farmer_application_by_email,
    get_farmer_application_by_username,
    get_farmer_application_by_id,
    get_all_farmer_applications,
    update_farmer_application,
    delete_farmer_application,
    approve_farmer_application,
    reject_farmer_application,
    delete_all_farmer_applications,
    get_all_approved_farmer_applications,
    get_all_rejected_farmer_applications,
    get_all_pending_farmer_applications,
)

from App.controllers.user import is_admin, get_user_by_email, get_user_by_username

farmer_application_views = Blueprint("farmer_application_views", __name__, template_folder="../templates")


@farmer_application_views.route("/farmer_applications", methods=["GET"])
@jwt_required()
def get_all_farmer_applications_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view all farmer applications"}), 403
    farmer_applications = get_all_farmer_applications()
    if farmer_applications:
        return jsonify([f_application.to_json() for f_application in farmer_applications]), 200
    return jsonify({"message": "No farmer applications found"}), 404


@farmer_application_views.route("/farmer_applications/<int:id>", methods=["GET"])
@jwt_required()
def get_farmer_application_by_id_action(id):
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view this farmer application"}), 403
    f_application = get_farmer_application_by_id(id)
    if f_application:
        return jsonify(f_application.to_json()), 200
    return jsonify({"message": "No farmer application found"}), 404


@farmer_application_views.route("/farmer_applications", methods=["POST"])
def create_farmer_application_action():
    data = request.json
    if data['username']:
        user = get_user_by_username(data['username'])
        if user:
            return jsonify({"message": "Username already exists"}), 400
    if data['email']:
        user = get_user_by_email(data['email'])
        if user:
            return jsonify({"message": "Email already exists"}), 400
    params = ['username', 'email', 'bio', 'phone', 'address', 'currency', 'units', 'avatar']
    for param in params:
        if not data[param]:
            return jsonify({"message": "Missing parameter: " + param}), 400
    f_application = create_farmer_application(username=data['username'], email=data['email'], bio=data['bio'], phone=data['phone'], address=data['address'], currency=data['currency'], units=data['units'], avatar=data['avatar'])
    if f_application:
        return jsonify(f_application.to_json()), 201
    return jsonify({"message": "Farmer application could not be created"}), 400


@farmer_application_views.route("/farmer_applications/<int:id>", methods=["PUT"])
@jwt_required()
def update_farmer_application_action(id):
    data = request.json
    f_application = get_farmer_application_by_id(id)
    if not f_application:
        return jsonify({"message": "No farmer application found"}), 404
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to update this farmer application"}), 403
    params = ['username', 'email', 'bio', 'phone', 'address', 'currency', 'units', 'avatar']
    for param in params:
        if not data[param]:
            return jsonify({"message": "Missing parameter: " + param}), 400
    f_application = update_farmer_application(id, username=data['username'], email=data['email'], bio=data['bio'], phone=data['phone'], address=data['address'], currency=data['currency'], units=data['units'], avatar=data['avatar'])
    if f_application:
        return jsonify(f_application.to_json()), 200
    return jsonify({"message": "Farmer application could not be updated"}), 400


@farmer_application_views.route("/farmer_applications/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_farmer_application_action(id):
    f_application = get_farmer_application_by_id(id)
    if not f_application:
        return jsonify({"message": "No farmer application found"}), 404
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to delete this farmer application"}), 403
    if delete_farmer_application(id):
        return jsonify({"message": "Farmer application deleted"}), 200
    return jsonify({"message": "Farmer application could not be deleted"}), 400


@farmer_application_views.route("/farmer_applications", methods=["DELETE"])
@jwt_required()
def delete_all_farmer_applications_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to delete all farmer applications"}), 403
    if delete_all_farmer_applications():
        return jsonify({"message": "All farmer applications deleted"}), 200
    return jsonify({"message": "All farmer applications could not be deleted"}), 400


@farmer_application_views.route("/farmer_applications/approve/<int:id>", methods=["PUT"])
@jwt_required()
def approve_farmer_application_action(id):
    f_application = get_farmer_application_by_id(id)
    if not f_application:
        return jsonify({"message": "No farmer application found"}), 404
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to approve this farmer application"}), 403
    if approve_farmer_application(id):
        return jsonify({"message": "Farmer application approved"}), 200
    return jsonify({"message": "Farmer application could not be approved"}), 400


@farmer_application_views.route("/farmer_applications/reject/<int:id>", methods=["PUT"])
@jwt_required()
def reject_farmer_application_action(id):
    f_application = get_farmer_application_by_id(id)
    if not f_application:
        return jsonify({"message": "No farmer application found"}), 404
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to reject this farmer application"}), 403
    if reject_farmer_application(id):
        return jsonify({"message": "Farmer application rejected"}), 200
    return jsonify({"message": "Farmer application could not be rejected"}), 400


@farmer_application_views.route("/farmer_applications/approved", methods=["GET"])
@jwt_required()
def get_all_approved_farmer_applications_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view all approved farmer applications"}), 403
    farmer_applications = get_all_approved_farmer_applications()
    if farmer_applications:
        return jsonify([f_application.to_json() for f_application in farmer_applications]), 200
    return jsonify({"message": "No approved farmer applications found"}), 404


@farmer_application_views.route("/farmer_applications/rejected", methods=["GET"])
@jwt_required()
def get_all_rejected_farmer_applications_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view all rejected farmer applications"}), 403
    farmer_applications = get_all_rejected_farmer_applications()
    if farmer_applications:
        return jsonify([f_application.to_json() for f_application in farmer_applications]), 200
    return jsonify({"message": "No rejected farmer applications found"}), 404


@farmer_application_views.route("/farmer_applications/pending", methods=["GET"])
@jwt_required()
def get_all_pending_farmer_applications_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view all pending farmer applications"}), 403
    farmer_applications = get_all_pending_farmer_applications()
    if farmer_applications:
        return jsonify([f_application.to_json() for f_application in farmer_applications]), 200
    return jsonify({"message": "No pending farmer applications found"}), 404


@farmer_application_views.route("/farmer_applications/username/", methods=["GET"])
@jwt_required()
def get_farmer_application_by_username_action():
    data = request.json
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view this farmer application"}), 403
    if data['username']:
        f_application = get_farmer_application_by_username(data['username'])
        if f_application:
            return jsonify(f_application.to_json()), 200
        return jsonify({"message": "No farmer application found"}), 404
    return jsonify({"message": "Missing parameter: username"}), 400


@farmer_application_views.route("/farmer_applications/email/", methods=["GET"])
@jwt_required()
def get_farmer_application_by_email_action():
    data = request.json
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view this farmer application"}), 403
    if data['email']:
        f_application = get_farmer_application_by_email(data['email'])
        if f_application:
            return jsonify(f_application.to_json()), 200
        return jsonify({"message": "No farmer application found"}), 404
    return jsonify({"message": "Missing parameter: email"}), 400
