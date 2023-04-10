from flask import (
    Blueprint,
    jsonify,
    request,
)
from flask_jwt import jwt_required, current_identity
import re

from App.controllers import (
    create_user,
    get_all_users_json,
    get_user_by_id,
    get_user_by_username,
    get_user_by_email,
    update_user,
    is_admin,
    check_password,
    create_log,
)

user_views = Blueprint("user_views", __name__, template_folder="../templates")


# Get all users
@user_views.route("/api/users", methods=["GET"])
@jwt_required()
def get_users_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view all users"}), 401
    users = get_all_users_json()
    if not users:
        return jsonify({"message": "No users found"}), 404
    return jsonify(users)


# Identify user
@user_views.route("/identify", methods=["GET"])
@jwt_required()
def identify():
    return jsonify(
        {
            "id": current_identity.id,
            "username": current_identity.username,
            "access": current_identity.access,
        }
    )


# Create normal user route
@user_views.route("/api/users", methods=["POST"])
def create_user_action():
    data = request.json
    if not data["email"] or not data["username"] or not data["password"]:
        return jsonify({"message": "Please fill out all fields"}), 400
    user = get_user_by_email(data["email"])
    if user:
        return jsonify({"message": "email already exists"}), 400
    user = get_user_by_username(data["username"])
    if user:
        return jsonify({"message": "username already exists"}), 400
    new_user = create_user(data["username"], data["email"], data["password"], access="user")
    if new_user:
        create_log(new_user.id, "User created", f"User {new_user.username} created")
        return jsonify(new_user.to_json()), 201
    return jsonify({"message": "User could not be created"}), 400


# Create admin user route
@user_views.route("/api/users/admin", methods=["POST"])
@jwt_required()
def create_admin_action():
    data = request.json
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to create an admin"}), 401
    user = get_user_by_email(data["email"])
    if user:
        return jsonify({"message": "email already exists"}), 400
    user = get_user_by_username(data["username"])
    if user:
        return jsonify({"message": "username already exists"}), 400
    new_user = create_user(data["username"], data["email"], data["password"], access="admin")
    if new_user:
        create_log(current_identity.id, "Admin created", f"User {new_user.username} created")
        return (
            jsonify(new_user.to_json()),
            201,
        )
    return jsonify({"message": "Admin could not be created"}), 400


# Get user by id
@user_views.route("/api/users/<int:id>", methods=["GET"])
def get_user_action(id):
    user = get_user_by_id(id)
    if user:
        return jsonify(user.to_json())
    return jsonify({"message": f"User {id} not found"}), 404


# Get user by email
@user_views.route("/api/users/email", methods=["GET"])
def get_user_by_email_action():
    data = request.json
    user = get_user_by_email(data["email"])
    if user:
        return jsonify(user.to_json())
    return jsonify({"message": f"{data['email']} not found"}), 404


# Get user by username
@user_views.route("/api/users/<string:username>", methods=["GET"])
def get_user_by_username_action(username):
    user = get_user_by_username(username)
    if user:
        return jsonify(user.to_json())
    return jsonify({"message": f"{username} not found"}), 404


# Update user
@user_views.route("/api/users/<int:id>", methods=["PUT"])
@jwt_required()
def update_user_action(id):
    if not is_admin(current_identity):
        if id != current_identity.id:
            return (
                jsonify({"message": "You are not authorized to update this user"}),
                401,
            )
    data = request.json
    user = get_user_by_id(id)
    if user:
        if "username" in data:
            if get_user_by_username(data["username"]):
                return jsonify({"message": "Username already exists"}), 400
            else:
                user = update_user(id=id, username=data["username"])
        if "email" in data:
            if get_user_by_email(data["email"]):
                return jsonify({"message": "Email already exists"}), 400
            else:
                user = update_user(id=id, email=data["email"])
        if "password" in data and "old_password" in data:
            if (
                len(data["password"]) < 8
                or not re.search(r"\d", data["password"])
                or not re.search(r"[A-Z]", data["password"])
                or not re.search(r"[a-z]", data["password"])
                or check_password(current_identity, data["password"])
                or not check_password(current_identity, data["old_password"])
            ):
                message = (
                    "-Password must be at least 8 characters.\n"
                    "-Password must contain at least one digit.\n"
                    "-Password must contain at least one uppercase letter.\n"
                    "-Password must contain at least one lowercase letter.\n"
                    "-New password must be different from the old password.\n"
                    "-Old password must be correct.\n"
                )
                return jsonify({"message": message}), 400
            else:
                user = update_user(id=id, password=data["password"])
        if "bio" in data:
            user = update_user(id=id, bio=data["bio"])
        if "phone" in data:
            user = update_user(id=id, phone=data["phone"])
        if "address" in data:
            user = update_user(id=id, address=data["address"])
        if "currency" in data:
            user = update_user(id=id, currency=data["currency"])
        if "units" in data:
            user = update_user(id=id, units=data["units"])
        if "avatar" in data:
            user = update_user(id=id, avatar=data["avatar"])
        create_log(current_identity.id, "User updated", f"User {user.username} updated")
        return jsonify(user.to_json()), 200
    return jsonify({"message": "User not found"}), 404
