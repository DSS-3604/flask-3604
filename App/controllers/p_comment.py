from App.models.p_comment import ProductComment
from App.database import db


def create_comment(product_id, user_id, body):
    new_comment = ProductComment(product_id=product_id, user_id=user_id, body=body)
    db.session.add(new_comment)
    db.session.commit()
    return new_comment


def get_all_comments():
    return ProductComment.query.all()


def get_all_comments_json():
    return [comment.to_json() for comment in get_all_comments()]


def get_comment_by_id(id):
    return ProductComment.query.get(id)


def get_comment_by_id_json(id):
    return get_comment_by_id(id).to_json()


def get_comments_by_product_id(product_id):
    return ProductComment.query.filter_by(product_id=product_id).all()


def get_comments_by_product_id_json(product_id):
    return [comment.to_json() for comment in get_comments_by_product_id(product_id)]


def get_comments_by_user_id(user_id):
    return ProductComment.query.filter_by(user_id=user_id).all()


def get_comments_by_user_id_json(user_id):
    return [comment.to_json() for comment in get_comments_by_user_id(user_id)]


def update_comment(id, body):
    comment = get_comment_by_id(id)
    if comment:
        comment.body = body
        db.session.add(comment)
        db.session.commit()
        return comment
    return None


def delete_comment(id):
    comment = get_comment_by_id(id)
    if comment:
        db.session.delete(comment)
        return db.session.commit()
    return None
