from App.models.query_reply import QueryReply
from App.controllers import get_user_by_id
from App.database import db
from datetime import datetime


def create_query_reply(query_id, user_id, body):
    new_reply = QueryReply(
        query_id=query_id,
        user_id=user_id,
        user_name=get_user_by_id(user_id).username,
        body=body,
    )
    db.session.add(new_reply)
    db.session.commit()
    return new_reply


def get_all_query_replies():
    return QueryReply.query.all()


def get_all_query_replies_json():
    return [reply.to_json() for reply in get_all_query_replies()]


def get_all_query_replies_by_query_id(query_id):
    return QueryReply.query.filter_by(query_id=query_id).all()


def get_all_query_replies_by_query_id_json(query_id):
    return [reply.to_json() for reply in get_all_query_replies_by_query_id(query_id)]


def get_query_reply_by_id(reply_id):
    return QueryReply.query.get(reply_id)


def get_query_reply_by_id_json(reply_id):
    return get_query_reply_by_id(reply_id).to_json()


def get_query_replies_by_user_id(user_id):
    return QueryReply.query.filter_by(user_id=user_id).all()


def get_query_replies_by_user_id_json(user_id):
    return [reply.to_json() for reply in get_query_replies_by_user_id(user_id)]


def get_query_replies_by_user_name(user_name):
    return QueryReply.query.filter_by(user_name=user_name).all()


def get_query_replies_by_user_name_json(user_name):
    return [reply.to_json() for reply in get_query_replies_by_user_name(user_name)]


def update_query_reply(reply_id, body):
    reply = get_query_reply_by_id(reply_id)
    if reply:
        reply.body = body
        reply.updated_timestamp = datetime.now()
        db.session.add(reply)
        db.session.commit()
        return reply
    return None


def delete_query_reply(reply_id):
    reply = get_query_reply_by_id(reply_id)
    if reply:
        db.session.delete(reply)
        db.session.commit()
        return reply
    return None
