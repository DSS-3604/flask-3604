from flask import Blueprint, jsonify
from flask_jwt import jwt_required, current_identity
import flask_excel as excel

from App.controllers.user import is_admin, get_all_users_json, get_all_farmers_json
from App.controllers.product import get_all_products_json, get_products_past_week_json
from App.controllers.product_category import get_product_categories_json
from App.controllers.contact_form import get_all_contact_forms_json
from App.controllers.farmer_application import get_all_farmer_applications_json
from App.controllers.farmer_review import get_all_reviews_json

# import all functions form /controllers/report.py
from App.controllers.report import (
    get_new_user_count,
    get_new_farmer_count,
    get_new_product_count,
    get_new_contact_form_count,
    get_new_product_category_count,
    get_total_user_count,
    get_total_farmer_count,
    get_product_count,
    get_total_category_count,
    get_total_contact_form_count,
    get_total_farmer_application_count,
    get_total_approved_farmer_application_count,
    get_total_rejected_farmer_application_count,
    get_total_pending_farmer_application_count,
    get_total_farmer_review_count,
    get_average_farmer_rating,
    get_new_product_count_by_farmer,
)


report_views = Blueprint("report_views", __name__, template_folder="../templates")


# Get all table counts
@report_views.route("/api/reports", methods=["GET"])
@jwt_required()
def get_reports_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view all reports"}), 401
    reports = {
        "new_user_count": get_new_user_count(),
        "new_farmer_count": get_new_farmer_count(),
        "new_product_count": get_new_product_count(),
        "new_contact_form_count": get_new_contact_form_count(),
        "new_product_category_count": get_new_product_category_count(),
        "total_user_count": get_total_user_count(),
        "total_farmer_count": get_total_farmer_count(),
        "total_product_count": get_product_count(),
        "total_product_category_count": get_total_category_count(),
        "total_contact_form_count": get_total_contact_form_count(),
        "total_farmer_application_count": get_total_farmer_application_count(),
        "total_approved_farmer_application_count": get_total_approved_farmer_application_count(),
        "total_rejected_farmer_application_count": get_total_rejected_farmer_application_count(),
        "total_pending_farmer_application_count": get_total_pending_farmer_application_count(),
        "total_farmer_review_count": get_total_farmer_review_count(),
        "average_farmer_rating": get_average_farmer_rating(),
        "farmers_and_recent_products": get_new_product_count_by_farmer(),
    }
    return jsonify(reports)


# Export all users to excel
@report_views.route("/api/reports/export/users", methods=["GET"])
@jwt_required()
def get_alL_users_report_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view all users"}), 401
    users = get_all_users_json()
    if not users:
        return jsonify({"message": "No users found"}), 404
    return excel.make_response_from_records(users, "csv")


# Export all farmers to excel
@report_views.route("/api/reports/export/farmers", methods=["GET"])
@jwt_required()
def get_farmers_report_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view all farmers/co-ops"}), 401
    farmers = get_all_farmers_json()
    if not farmers:
        return jsonify({"message": "No farmers/co-ops found"}), 404
    return excel.make_response_from_records(farmers, "csv")


# Export all products to excel
@report_views.route("/api/reports/export/products", methods=["GET"])
@jwt_required()
def get_products_report_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view all products"}), 401
    products = get_all_products_json()
    if not products:
        return jsonify({"message": "No products found"}), 404
    return excel.make_response_from_records(products, "csv")


# export all products created in the last 7 days to excel
@report_views.route("/api/reports/export/products/week", methods=["GET"])
@jwt_required()
def get_products_report_week_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view all products"}), 401
    products = get_products_past_week_json()
    if not products:
        return jsonify({"message": "No products found"}), 404
    return excel.make_response_from_records(products, "csv")


# Export all product categories to excel
@report_views.route("/api/reports/export/product_categories", methods=["GET"])
@jwt_required()
def get_product_categories_report_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view all product categories"}), 401
    product_categories = get_product_categories_json()
    if not product_categories:
        return jsonify({"message": "No product categories found"}), 404
    return excel.make_response_from_records(product_categories, "csv")


# Export all contact forms to excel
@report_views.route("/api/reports/export/contact_forms", methods=["GET"])
@jwt_required()
def get_contact_forms_report_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view all contact forms"}), 401
    contact_forms = get_all_contact_forms_json()
    if not contact_forms:
        return jsonify({"message": "No contact forms found"}), 404
    return excel.make_response_from_records(contact_forms, "csv")


# Export all farmer applications to excel
@report_views.route("/api/reports/export/farmer_applications", methods=["GET"])
@jwt_required()
def get_farmer_applications_report_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view all farmer applications"}), 401
    farmer_applications = get_all_farmer_applications_json()
    if not farmer_applications:
        return jsonify({"message": "No farmer applications found"}), 404
    return excel.make_response_from_records(farmer_applications, "csv")


# Export all farmer reviews to excel
@report_views.route("/api/reports/export/farmer_reviews", methods=["GET"])
@jwt_required()
def get_farmer_reviews_report_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view all farmer reviews"}), 401
    farmer_reviews = get_all_reviews_json()
    if not farmer_reviews:
        return jsonify({"message": "No farmer reviews found"}), 404
    return excel.make_response_from_records(farmer_reviews, "csv")


