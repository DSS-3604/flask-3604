from App.models.farmer_review import FarmerReview
from App.controllers.user import get_user_by_id
from App.database import db
from datetime import datetime


def create_review(farmer_id, user_id, rating, body):
    new_review = FarmerReview(
        farmer_id=farmer_id,
        farmer_name=get_user_by_id(farmer_id).username,
        user_id=user_id,
        user_name=get_user_by_id(user_id).username,
        user_avatar=get_user_by_id(user_id).avatar,
        rating=rating,
        body=body,
    )
    db.session.add(new_review)
    db.session.commit()
    return new_review


def get_all_reviews():
    return FarmerReview.query.all()


def get_all_reviews_json():
    return [review.to_json() for review in get_all_reviews()]


def get_review_by_id(id):
    return FarmerReview.query.get(id)


def get_review_by_id_json(id):
    return get_review_by_id(id).to_json()


def get_reviews_by_farmer_id(farmer_id):
    return FarmerReview.query.filter_by(farmer_id=farmer_id).all()


def get_reviews_by_farmer_id_json(farmer_id):
    return [review.to_json() for review in get_reviews_by_farmer_id(farmer_id)]


def get_reviews_by_user_id(user_id):
    return FarmerReview.query.filter_by(user_id=user_id).all()


def get_reviews_by_user_id_json(user_id):
    return [review.to_json() for review in get_reviews_by_user_id(user_id)]


def update_review(id, rating, body):
    review = get_review_by_id(id)
    if review:
        review.rating = rating
        review.body = body
        review.updated_timestamp = datetime.now()
        db.session.add(review)
        db.session.commit()
        return review
    return None


def delete_review(id):
    review = get_review_by_id(id)
    if review:
        db.session.delete(review)
        return db.session.commit()
    return None
