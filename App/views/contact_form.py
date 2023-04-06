from flask import Blueprint, jsonify, request

from flask_jwt import jwt_required, current_identity

from App.controllers.contact_form import (
    create_contact_form,
    get_contact_form_by_id,
    get_all_contact_forms,
    update_contact_form_by_id,
    delete_contact_form_by_id,
)

from App.controllers.logging import create_log

from App.controllers.user import is_admin

contact_form_views = Blueprint(
    "contact_form_views", __name__, template_folder="../templates"
)


@contact_form_views.route("/contact_forms", methods=["GET"])
@jwt_required()
def get_all_contact_forms_action():
    if not is_admin(current_identity):
        return (
            jsonify({"message": "You are not authorized to view all contact forms"}),
            403,
        )
    contact_forms = get_all_contact_forms()
    if contact_forms:
        return (
            jsonify([contact_form.to_json() for contact_form in contact_forms]),
            200,
        )
    return jsonify({"message": "No contact forms found"}), 404


@contact_form_views.route("/contact_forms/<int:id>", methods=["GET"])
@jwt_required()
def get_contact_form_by_id_action(id):
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view this contact form"}), 403
    contact_form = get_contact_form_by_id(id)
    if contact_form:
        return jsonify(contact_form.to_json()), 200
    return jsonify({"message": "No contact form found"}), 404


@contact_form_views.route("/contact_forms", methods=["POST"])
def create_contact_form_action():
    data = request.json
    params = ["name", "phone", "email", "message"]
    if not all(param in data for param in params):
        return jsonify({"message": "Missing parameters"}), 400

    contact_form = create_contact_form(data["name"], data["phone"], data["email"], data["message"])
    if contact_form:
        return jsonify(contact_form.to_json()), 201
    return jsonify({"message": "Could not create contact form"}), 400


@contact_form_views.route("/contact_forms/<int:id>", methods=["PUT"])
@jwt_required()
def update_contact_form_by_id_action(id):
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to update contact forms"}), 403
    data = request.json
    params = ["name", "phone", "email", "message"]
    if not all(param in data for param in params):
        return jsonify({"message": "Missing parameters"}), 400
    contact_form = update_contact_form_by_id(id, data["name"], data["phone"], data["email"], data["message"])
    if contact_form:
        create_log(current_identity.id, "Contact Form Updated", f"Contact Form {id} updated")
        return jsonify(contact_form.to_json()), 200
    return jsonify({"message": "Could not update contact form"}), 400


@contact_form_views.route("/contact_forms/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_contact_form_by_id_action(id):
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to delete contact forms"}), 403
    contact_form = get_contact_form_by_id(id)
    if contact_form:
        if delete_contact_form_by_id(id):
            create_log(current_identity.id, "Contact Form Deleted", f"Contact Form {id} deleted")
            return jsonify({"message": "Contact form deleted"}), 200
    return jsonify({"message": "Could not delete contact form"}), 400


