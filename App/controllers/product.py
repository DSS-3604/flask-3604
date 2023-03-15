from App.database import db
from App.models.product import Product
from datetime import datetime, timedelta


def create_product(name, description, image, retail_price, product_quantity, farmer_id):
    product = Product(
        name, description, image, retail_price, product_quantity, farmer_id
    )
    db.session.add(product)
    db.session.commit()
    return product


def get_products_past_week():
    return Product.query.filter(Product.created_at >= datetime.now() - timedelta(days=7)).all()


def get_products_past_week_json():
    return [product.to_json() for product in get_products_past_week()]


def get_products_past_month():
    return Product.query.filter(Product.created_at >= datetime.now() - timedelta(days=30)).all()


def get_products_past_month_json():
    return [product.to_json() for product in get_products_past_month()]


def get_products_past_year():
    return Product.query.filter(Product.created_at >= datetime.now() - timedelta(days=365)).all()


def get_products_past_year_json():
    return [product.to_json() for product in get_products_past_year()]


def get_products_past_week_by_farmer_id(farmer_id):
    return Product.query.filter(Product.created_at >= datetime.now() - timedelta(days=7)).filter_by(
        farmer_id=farmer_id).all()


def get_all_products():
    return Product.query.all()


def get_all_products_json():
    return [product.to_json() for product in get_all_products()]


def get_product_by_id(id):
    return Product.query.get(id)


def get_product_by_id_json(id):
    return get_product_by_id(id).to_json()


def get_products_by_farmer_id(farmer_id):
    return Product.query.filter_by(farmer_id=farmer_id).all()


def get_products_by_farmer_id_json(farmer_id):
    return [product.to_json() for product in get_products_by_farmer_id(farmer_id)]


def get_products_by_name(name):
    return Product.query.filter_by(name=name).all()


def get_products_by_name_json(name):
    return [product.to_json() for product in get_products_by_name(name)]


def update_product(id, name="", description="", image="", retail_price="", product_quantity=""):
    product = get_product_by_id(id)
    if product:
        if name:
            product.name = name
        if description:
            product.description = description
        if image:
            product.image = image
        if retail_price:
            product.retail_price = retail_price
        if product_quantity:
            product.product_quantity = product_quantity
        db.session.add(product)
        return db.session.commit()
    return None


def delete_product(id):
    product = get_product_by_id(id)
    if product:
        db.session.delete(product)
        return db.session.commit()
    return None
