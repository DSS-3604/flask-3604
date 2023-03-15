from App.models import farmer_application
from App.controllers.user import create_farmer, get_user_by_email, get_user_by_username
from App.database import db


def create_farmer_application(username, email, bio, phone, address, currency="USD", units="kg", avatar=""):
    farmer1 = get_user_by_email(email)
    farmer2 = get_user_by_username(username)

    if farmer1 or farmer2:
        return None

    new_farmer_application = farmer_application.FarmerApplication(
        username=username,
        email=email,
        bio=bio,
        phone=phone,
        address=address,
        currency=currency,
        units=units,
        avatar=avatar,
    )
    db.session.add(new_farmer_application)
    db.session.commit()
    return new_farmer_application


def get_farmer_application_by_email(email):
    return farmer_application.FarmerApplication.query.filter_by(email=email).first()


def get_farmer_application_by_username(username):
    return farmer_application.FarmerApplication.query.filter_by(username=username).first()


def get_farmer_application_by_id(id):
    return farmer_application.FarmerApplication.query.filter_by(id=id).first()


def get_all_farmer_applications():
    return farmer_application.FarmerApplication.query.all()


def update_farmer_application(id, username, email, bio, phone, address, currency="USD", units="kg", avatar=""):
    f_application = get_farmer_application_by_id(id)
    if f_application:
        f_application.username = username
        f_application.email = email
        f_application.bio = bio
        f_application.phone = phone
        f_application.address = address
        f_application.currency = currency
        f_application.units = units
        f_application.avatar = avatar
        db.session.commit()
        return True
    return False


def approve_farmer_application(id, comment=""):
    f_application = get_farmer_application_by_id(id)
    if f_application:
        farmer = create_farmer(
            f_application.username,
            f_application.email,
            f_application.password,
            f_application.bio,
            f_application.phone,
            f_application.address,
            f_application.currency,
            f_application.units,
            f_application.avatar,
        )
        f_application.status = f"Approved: {comment}"
        return farmer
    return False


def reject_farmer_application(id, comment=""):
    f_application = get_farmer_application_by_id(id)
    if f_application:
        f_application.status = f"Rejected: {comment}"
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
    db.session.commit()
    return True


def get_all_approved_farmer_applications():
    return farmer_application.FarmerApplication.query.filter_by(status="Approved").all()


def get_all_rejected_farmer_applications():
    return farmer_application.FarmerApplication.query.filter_by(status="Rejected").all()


def get_all_pending_farmer_applications():
    return farmer_application.FarmerApplication.query.filter_by(status="Pending").all()
