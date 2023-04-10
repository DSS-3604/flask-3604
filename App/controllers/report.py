from App.models.user import User
from App.models.farmer_application import FarmerApplication
from App.models.product import Product
from App.models.contact_form import ContactForm
from App.models.product_category import ProductCategory
from App.models.farmer_review import FarmerReview

from datetime import datetime, timedelta


# function to return number of users created in the past week
def get_new_user_count():
    return User.query.filter(User.timestamp >= datetime.now() - timedelta(days=7)).count()


# function to return number of farmer applications approved in the past week
def get_new_farmer_count():
    return FarmerApplication.query.filter(
        FarmerApplication.updated_timestamp >= datetime.now() - timedelta(days=7),
        FarmerApplication.status == "approved",
    ).count()


# function to get the total product count
def get_total_product_count():
    return Product.query.count()


# function to return number of products created in the past week
def get_new_product_count():
    return Product.query.filter(Product.timestamp >= datetime.now() - timedelta(days=7)).count()


# function to return number of contact form messages created in the past week
def get_new_contact_form_count():
    return ContactForm.query.filter(ContactForm.timestamp >= datetime.now() - timedelta(days=7)).count()


# function to return number of product categories created in the past week
def get_new_product_category_count():
    return ProductCategory.query.filter(ProductCategory.timestamp >= datetime.now() - timedelta(days=7)).count()


# function to return total number of users
def get_total_user_count():
    return User.query.count()


# function to return total number of farmers
def get_total_farmer_count():
    return User.query.filter(User.access == "farmer").count()


# function to return total number of products
def get_product_count():
    return Product.query.count()


# function to return total number of product categories
def get_total_category_count():
    return ProductCategory.query.count()


# function to return total number of contact form messages
def get_total_contact_form_count():
    return ContactForm.query.count()


# function to return total number of farmer applications
def get_total_farmer_application_count():
    return FarmerApplication.query.count()


# function to return total number of approved farmer applications
def get_total_approved_farmer_application_count():
    return FarmerApplication.query.filter(FarmerApplication.status == "approved").count()


# function to return total number of pending farmer applications
def get_total_pending_farmer_application_count():
    return FarmerApplication.query.filter(FarmerApplication.status == "pending").count()


# function to return total number of rejected farmer applications
def get_total_rejected_farmer_application_count():
    return FarmerApplication.query.filter(FarmerApplication.status == "rejected").count()


# function to return total number of farmer reviews
def get_total_farmer_review_count():
    return FarmerReview.query.count()


# function to return average rating of all farmer reviews
def get_average_farmer_rating():
    reviews = FarmerReview.query.all()
    if len(reviews) == 0:
        return 0
    else:
        return sum([review.rating for review in reviews]) / len(reviews)


# function to get farmers and the number of products they have that have been created or updated in the past week
def get_new_product_count_by_farmer():
    farmers = User.query.filter(User.access == "farmer").all()
    new_product_count_by_farmer = {}
    for farmer in farmers:
        new_product_count_by_farmer[farmer.username] = Product.query.filter(
            Product.farmer_id == farmer.id,
            Product.timestamp >= datetime.now() - timedelta(days=7),
        ).count()
    return new_product_count_by_farmer
