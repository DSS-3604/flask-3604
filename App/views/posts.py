from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required


from App.controllers import (
    get_user_by_id,
    create_post,
    get_all_posts,
    get_all_posts_json,
)

posts_views = Blueprint("posts_views", __name__, template_folder="../templates")

# Get posts
@posts_views.route("/api/posts", methods=["GET"])
def get_posts_action():
    posts = get_all_posts()
    if posts:
        return jsonify(get_all_posts_json()), 200
    else:
        return jsonify({"message": "No Posts exist"}), 404