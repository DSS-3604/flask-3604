from App.models.logging import Logging
from App.controllers import get_user_by_id
from App.database import db
from datetime import datetime


def create_log(user_id, action, description):
    new_log = Logging(user_id=user_id, user_name=get_user_by_id(user_id).username, action=action, description=description)
    db.session.add(new_log)
    db.session.commit()
    return new_log


def get_all_logs():
    return Logging.query.all()


def get_all_logs_json():
    return [log.to_json() for log in get_all_logs()]


def get_log_by_id(id):
    return Logging.query.get(id)


def get_log_by_id_json(id):
    return get_log_by_id(id).to_json()


def get_logs_by_user_id(user_id):
    return Logging.query.filter_by(user_id=user_id).all()


def get_logs_by_user_id_json(user_id):
    return [log.to_json() for log in get_logs_by_user_id(user_id)]


def get_logs_by_action(action):
    return Logging.query.filter_by(action=action).all()


def get_logs_by_action_json(action):
    return [log.to_json() for log in get_logs_by_action(action)]


def get_logs_by_user_name(user_name):
    return Logging.query.filter_by(user_name=user_name).all()


def get_logs_by_user_name_json(user_name):
    return [log.to_json() for log in get_logs_by_user_name(user_name)]