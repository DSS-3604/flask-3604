import os
from flask import Flask
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from datetime import timedelta
import flask_excel as excel

from App.database import create_db

from App.controllers import setup_jwt

from App.views import views


def add_views(app):
    for view in views:
        app.register_blueprint(view)


def loadConfig(app, config):
    app.config["ENV"] = os.environ.get("ENV", "DEVELOPMENT")
    delta = 7
    if app.config["ENV"] == "DEVELOPMENT":
        app.config.from_object("App.config")
        delta = app.config["JWT_EXPIRATION_DELTA"]
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
        app.config["DEBUG"] = os.environ.get("ENV").upper() != "PRODUCTION"
        app.config["ENV"] = os.environ.get("ENV")
        delta = os.environ.get("JWT_EXPIRATION_DELTA", 7)

    app.config["JWT_EXPIRATION_DELTA"] = timedelta(days=int(delta))

    for key, value in config.items():
        app.config[key] = config[key]


def create_app(config={}):
    app = Flask(__name__, static_url_path="/static")
    CORS(app)
    loadConfig(app, config)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEVER_NAME"] = "0.0.0.0"
    app.config["PREFERRED_URL_SCHEME"] = "https"
    app.config["UPLOADED_PHOTOS_DEST"] = "App/uploads"
    photos = UploadSet("photos", TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    excel.init_excel(app)
    add_views(app)
    create_db(app)
    setup_jwt(app)
    with app.app_context() as app_context:
        from App.controllers.user import create_su, create_default_farmer
        create_su()
        create_default_farmer()
        app_context.push()
    return app
