from App.database import db
from App.models.product import Product
from App.controllers.user import get_user_by_id
from App.controllers.product_category import get_product_category_by_id_json
from datetime import datetime, timedelta


def create_product(
    farmer_id,
    category_id,
    name,
    description,
    image=None,
    retail_price=1,
    wholesale_price=1,
    wholesale_unit_quantity=1,
    total_product_quantity=1,
):
    product = Product(
        farmer_id=farmer_id,
        farmer_name=get_user_by_id(farmer_id).username,
        category_id=category_id,
        category_name=get_product_category_by_id_json(category_id)["name"],
        name=name,
        description=description,
        image=image,
        retail_price=retail_price,
        wholesale_price=wholesale_price,
        wholesale_unit_quantity=wholesale_unit_quantity,
        total_product_quantity=total_product_quantity,
    )
    db.session.add(product)
    db.session.commit()
    return product


def search_products_by_name_json(name):
    products = Product.query.filter().all()
    return [product.to_json() for product in products if name in product.name]


def search_products_by_name_past_week_json(name):
    products = get_products_past_week()
    return [product.to_json() for product in products if name in product.name]


def get_products_by_category_id(category_id):
    return Product.query.filter_by(category_id=category_id).all()


def get_products_by_category_id_json(category_id):
    return [product.to_json() for product in get_products_by_category_id(category_id)]


def get_products_past_week():
    return Product.query.filter(
        Product.timestamp >= datetime.now() - timedelta(days=7)
    ).all()


def get_products_past_week_json():
    return [product.to_json() for product in get_products_past_week()]


def get_products_past_month():
    return Product.query.filter(
        Product.timestamp >= datetime.now() - timedelta(days=30)
    ).all()


def get_products_past_month_json():
    return [product.to_json() for product in get_products_past_month()]


def get_products_past_year():
    return Product.query.filter(
        Product.timestamp >= datetime.now() - timedelta(days=365)
    ).all()


def get_products_past_year_json():
    return [product.to_json() for product in get_products_past_year()]


def get_products_past_week_by_farmer_id(farmer_id):
    return (
        Product.query.filter(Product.timestamp >= datetime.now() - timedelta(days=7))
        .filter_by(farmer_id=farmer_id)
        .all()
    )


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


def update_product(
    id,
    category_id=None,
    name=None,
    description=None,
    image=None,
    retail_price=None,
    wholesale_price=None,
    wholesale_unit_quantity=None,
    total_product_quantity=None,
):
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
        if wholesale_price:
            product.wholesale_price = wholesale_price
        if wholesale_unit_quantity:
            product.wholesale_unit_quantity = wholesale_unit_quantity
        if total_product_quantity:
            product.total_product_quantity = total_product_quantity
        if category_id:
            product.category_id = category_id
            product.category_name = get_product_category_by_id_json(category_id)["name"]
        product.updated_timestamp = datetime.now()
        db.session.add(product)
        db.session.commit()
        return product
    return None


def delete_product(id):
    product = get_product_by_id(id)
    if product:
        db.session.delete(product)
        return db.session.commit()
    return None
