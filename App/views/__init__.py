from .user import user_views
from .index import index_views
from .product import product_views
from .p_comment import comment_views
from .p_reply import reply_views
from .farmer_review import review_views
from .farmer_application import farmer_application_views
from .product_category import product_category_views
from .contact_form import contact_form_views
from .report import report_views
from .logging import logging_views
from .product_query import product_query_views

views = [
    user_views,
    index_views,
    product_views,
    comment_views,
    reply_views,
    review_views,
    farmer_application_views,
    product_category_views,
    contact_form_views,
    report_views,
    logging_views,
]
