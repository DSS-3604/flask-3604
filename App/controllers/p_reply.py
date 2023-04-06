from App.models.p_reply import ProductReply
from App.controllers import get_user_by_id
from App.database import db
from datetime import datetime


def create_reply(comment_id, user_id, body):
    new_reply = ProductReply(p_comment_id=comment_id, user_id=user_id, user_name=get_user_by_id(user_id).username, body=body)
    db.session.add(new_reply)
    db.session.commit()
    return new_reply


def get_all_replies_by_comment_id(comment_id):
    return ProductReply.query.filter_by(p_comment_id=comment_id).all()


def get_all_replies_by_comment_id_json(comment_id):
    return [reply.to_json() for reply in get_all_replies_by_comment_id(comment_id)]


def get_reply_by_id(reply_id):
    return ProductReply.query.get(reply_id)


def get_reply_by_id_json(reply_id):
    return get_reply_by_id(reply_id).to_json()


def get_replies_by_user_id(user_id):
    return ProductReply.query.filter_by(user_id=user_id).all()


def get_replies_by_user_id_json(user_id):
    return [reply.to_json() for reply in get_replies_by_user_id(user_id)]


def update_reply(reply_id, body):
    reply = get_reply_by_id(reply_id)
    if reply:
        reply.body = body
        reply.updated_timestamp = datetime.now()
        db.session.add(reply)
        db.session.commit()
        return reply
    return None


def delete_reply(reply_id):
    reply = get_reply_by_id(reply_id)
    if reply:
        db.session.delete(reply)
        return db.session.commit()
    return None
