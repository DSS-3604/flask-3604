from flask import (
    Blueprint,
    render_template,
    jsonify,
)

index_views = Blueprint("index_views", __name__, template_folder="../templates")


@index_views.route("/", methods=["GET"])
def index_page():
    return render_template("index.html")


@index_views.route("/healthcheck", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})
