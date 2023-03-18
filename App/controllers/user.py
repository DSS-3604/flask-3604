from App.models.user import User, ACCESS
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


def create_farmer(
    username,
    email,
    password,
    bio,
    phone,
    address,
    currency="USD",
    units="kg",
    avatar="",
):
    return create_user(
        username,
        email,
        password,
        "farmer",
        bio=bio,
        phone=phone,
        address=address,
        currency=currency,
        units=units,
        avatar=avatar,
    )


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        print(user.to_json())
        return user
    return None


def get_user_by_id(id):
    return User.query.get(id)


def get_all_users():
    return User.query.all()


def get_all_users_json():
    return [user.to_json() for user in get_all_users()]


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
        return db.session.commit()
    return None


def is_admin(user):
    return user.get_access() == ACCESS["admin"]


def is_farmer(user):
    return user.get_access() == ACCESS["farmer"]


def check_password(user, password):
    return user.check_password(password)


def create_su():
    user = create_admin('admin123', 'admin123@gmail.com', 'admin123')
    db.session.add(user)
    return db.session.commit()
