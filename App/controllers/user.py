from App.models.user import User
from App.database import db


def create_user(
    username,
    email,
    password,
    access="user",
    bio="",
    phone="",
    address="",
    currency="USD",
    units="kg",
    avatar="",
):
    user1 = get_user_by_email(email)
    user2 = get_user_by_username(username)
    if user1 or user2:
        return None
    new_user = User(
        username=username,
        email=email,
        password=password,
        access=access,
        bio=bio,
        phone=phone,
        address=address,
        currency=currency,
        units=units,
        avatar=avatar,
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user


def create_admin(username, email, password):
    return create_user(
        username,
        email,
        password,
        "admin",
        bio="",
        phone="",
        address="",
        currency="USD",
        units="kg",
        avatar="",
    )


def update_access(id, access):
    user = get_user_by_id(id)
    if user:
        user.access = access
        db.session.add(user)
        db.session.commit()
        return user
    return None


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user
    return None


def get_user_by_id(id):
    return User.query.get(id)


def get_all_users():
    return User.query.all()


def get_all_users_json():
    return [user.to_json() for user in get_all_users()]


def get_all_farmers():
    return User.query.filter_by(access="farmer").all()


def get_all_farmers_json():
    return [farmer.to_json() for farmer in get_all_farmers()]


def get_all_admins():
    return User.query.filter_by(access="admin").all()


def get_all_admins_json():
    return [admin.to_json() for admin in get_all_admins()]


def update_user(
    id,
    username="",
    email="",
    password="",
    bio="",
    phone="",
    address="",
    currency="",
    units="",
    avatar="",
):
    user = get_user_by_id(id)
    if user:
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.set_password(password)
        if bio:
            user.bio = bio
        if phone:
            user.phone = phone
        if address:
            user.address = address
        if currency:
            user.currency = currency
        if units:
            user.units = units
        if avatar:
            user.avatar = avatar
        db.session.add(user)
        db.session.commit()
        return user
    return None


def is_admin(user):
    return user.get_access() == "admin"


def is_farmer(user):
    return user.get_access() == "farmer"


def check_password(user, password):
    return user.check_password(password)


def create_su():
    user = get_user_by_username("admin123")
    if not user:
        user = create_admin("admin123", "admin123@gmail.com", "admin123")
        print("admin created")
        db.session.add(user)
        return db.session.commit()
    return None


def create_default_farmer():
    farmer1 = get_user_by_username("farmer123")
    farmer2 = get_user_by_email("farmer123@gmail.com")
    if not farmer1 and not farmer2:
        from App.controllers.farmer_application import (
            create_farmer_application,
            approve_farmer_application,
        )

        user = create_user(
            "farmer123",
            "farmer123@gmail.com",
            "farmer123",
            "i want to be a farmer",
            "800-1234",
            "University Drive",
        )
        farmer_application = create_farmer_application(
            user.id, "default farmer account"
        )
        approve_farmer_application(farmer_application.id)
        print("farmer created")
        db.session.add(farmer_application)
        db.session.add(user)
        return db.session.commit()
    return None
