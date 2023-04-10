from App.models.product_category import ProductCategory
from App.database import db
from datetime import datetime


def get_products_by_category_name(name):
    return ProductCategory.query.filter_by(name=name).first().products


def get_products_by_category_name_json(name):
    return [product.to_json() for product in get_products_by_category_name(name)]


def get_product_categories():
    return ProductCategory.query.all()


def get_product_categories_json():
    return [product_category.to_json() for product_category in get_product_categories()]


def get_product_category_by_id(id):
    return ProductCategory.query.get(id)


def get_product_category_by_id_json(id):
    return get_product_category_by_id(id).to_json()


def get_product_category_by_name(name):
    return ProductCategory.query.filter_by(name=name).all()


def get_product_category_by_name_json(name):
    return [product_category.to_json() for product_category in get_product_category_by_name(name)]


def update_product_category(id, name):
    product_category = get_product_category_by_id(id)
    if product_category:
        if name:
            product_category.name = name
            product_category.updated_timestamp = datetime.now()
            db.session.add(product_category)
            db.session.commit()
            return product_category
    return None


def create_product_category(name):
    pc = get_product_category_by_name(name)
    if not pc:
        product_category = ProductCategory(name)
        db.session.add(product_category)
        db.session.commit()
        return product_category
    return None


def delete_product_category(id):
    product_category = get_product_category_by_id(id)
    if product_category:
        db.session.delete(product_category)
        return db.session.commit()
    return None
