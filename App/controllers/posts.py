from App.models import Post
from App.controllers import get_user
from App.database import db

def create_post(poster_id, post_title, post_description):
    poster = get_user(poster_id)
    if poster:
        post = Post(post_title, post_description)
        db.session.add(post)
        db.session.commit()
        return post
    return None

def get_all_posts():
    posts = Post.query.all()
    return posts

def get_all_posts_json():
    posts = Post.query.all()
    return [posts.to_json() for post in posts]