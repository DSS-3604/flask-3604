from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required, current_identity

# import all functions form /controllers/report.py
from App.controllers.report import *


report_views = Blueprint("report_views", __name__, template_folder="../templates")


# Get all reports
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
        "farmers_and_recent_products": get_new_products_by_farmer(),
    }
    return jsonify(reports)
