from App.models.farmer_application import FarmerApplication
from App.controllers.user import update_access, get_user_by_id
from App.database import db
import datetime


def create_farmer_application(user_id, comment):
    f_application = get_farmer_application_by_user_id(user_id)
    if f_application:
        if f_application.status == "Pending" or f_application.status == "Approved":
            return None
    new_f_application = FarmerApplication(user_id=user_id, user_name=get_user_by_id(user_id).username, comment=comment)
    db.session.add(new_f_application)
    db.session.commit()
    return new_f_application


def get_farmer_application_by_id(id):
    return FarmerApplication.query.filter_by(id=id).first()


def get_farmer_application_by_user_id(user_id):
    return FarmerApplication.query.filter_by(user_id=user_id).first()


def get_all_farmer_applications():
    return FarmerApplication.query.all()


def get_all_farmer_applications_json():
    return [f_application.to_json() for f_application in get_all_farmer_applications()]


def update_farmer_application(id, status="", comment=""):
    f_application = get_farmer_application_by_id(id)
    if f_application:
        if status:
            f_application.status = status
        if comment:
            f_application.comment = comment
        f_application.updated_timestamp = datetime.datetime.now()
        db.session.add(f_application)
        db.session.commit()
        return f_application
    return None


def approve_farmer_application(id):
    f_application = get_farmer_application_by_id(id)
    if f_application:
        if f_application.status == "Pending":
            update_farmer_application(id=id, status="Approved")
            update_access(f_application.user_id, "farmer")
            return True
    return False


def reject_farmer_application(id):
    f_application = get_farmer_application_by_id(id)
    if f_application:
        if f_application.status == "Pending":
            update_farmer_application(id=id, status="Rejected")
            return True
    return False


def delete_farmer_application(id):
    f_application = get_farmer_application_by_id(id)
    if f_application:
        db.session.delete(f_application)
        db.session.commit()
        return True
    return False


def delete_all_farmer_applications():
    f_applications = get_all_farmer_applications()
    for f_application in f_applications:
        db.session.delete(f_application)
    return db.session.commit()


def get_all_approved_farmer_applications():
    return FarmerApplication.query.filter_by(status="Approved").all()


def get_all_rejected_farmer_applications():
    return FarmerApplication.query.filter_by(status="Rejected").all()


def get_all_pending_farmer_applications():
    return FarmerApplication.query.filter_by(status="Pending").all()
