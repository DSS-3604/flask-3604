from .user import user_views
from .index import index_views
from .product import product_views
from .p_comment import comment_views
from .p_reply import reply_views
from .farmer_review import review_views

views = [
    user_views,
    index_views,
    product_views,
    comment_views,
    reply_views,
    review_views,
]
