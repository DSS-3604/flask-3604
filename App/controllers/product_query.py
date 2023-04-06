from App.models.product_query import ProductQuery
from App.controllers.user import get_user_by_id
from App.controllers.product import get_product_by_id
from App.database import db


def create_product_query(user_id, product_id, message):
    product = get_product_by_id(product_id)
    if not product:
        return None
    user = get_user_by_id(user_id)
    if not user:
        return None
    farmer = get_user_by_id(product.farmer_id)
    if not farmer:
        return None
    product_query = ProductQuery(
        user_id=user.id,
        user_name=user.username,
        product_id=product.id,
        product_name=product.name,
        farmer_id=farmer.id,
        farmer_name=farmer.username,
        email=user.email,
        phone=user.phone,
        message=message,
    )
    if not product_query:
        return None
    db.session.add(product_query)
    db.session.commit()
    return product_query


def get_product_query_by_id(id):
    product_query = ProductQuery.query.filter_by(id=id).first()
    return product_query


def get_product_query_by_user_id(user_id):
    product_query = ProductQuery.query.filter_by(user_id=user_id).all()
    return product_query


def get_product_query_by_product_id(product_id):
    product_query = ProductQuery.query.filter_by(product_id=product_id).all()
    return product_query


def get_product_query_by_farmer_id(farmer_id):
    product_query = ProductQuery.query.filter_by(farmer_id=farmer_id).all()
    return product_query


def get_product_query_by_id_json(id):
    product_query = get_product_query_by_id(id)
    if product_query:
        return product_query.to_json()
    return None


def get_product_query_by_user_id_json(user_id):
    product_query = get_product_query_by_user_id(user_id)
    if product_query:
        return [p.to_json() for p in product_query]
    return None


def get_product_query_by_product_id_json(product_id):
    product_query = get_product_query_by_product_id(product_id)
    if product_query:
        return [p.to_json() for p in product_query]
    return None


def get_product_query_by_farmer_id_json(farmer_id):
    product_query = get_product_query_by_farmer_id(farmer_id)
    if product_query:
        return [p.to_json() for p in product_query]
    return None


def get_all_product_queries():
    product_query = ProductQuery.query.all()
    return product_query


def get_all_product_queries_json():
    product_query = get_all_product_queries()
    if product_query:
        return [p.to_json() for p in product_query]
    return None


def delete_product_query(id):
    product_query = get_product_query_by_id(id)
    if product_query:
        db.session.delete(product_query)
        db.session.commit()
        return True
    return False
