import datetime
from app import db
from app.vendor.models.product import Product


class ProductDao:

    @staticmethod
    def save_product(product):
        db.session.add(product)
        db.session.commit()
        db.session.refresh(product)
        return product

    @staticmethod
    def update_product(product):
        existing_product = ProductDao.get_by_id(product.id)        
        if product.product_name:
            existing_product.product_name = product.product_name

        if product.department:
            existing_product.deparment = product.department
        
        if product.budget_owner:
            existing_product.budget_owner = product.budget_owner

        if product.product_owner:
            existing_product.product_owner = product.product_owner

        if product.expiration_date:            
            existing_product.expiration_date = product.expiration_date

        if product.payment_method:
            existing_product.payment_method = product.payment_method

        if product.product_type:
            existing_product.product_type = product.product_type

        if product.status:
            existing_product.status = product.status

        if product.user_by:
            existing_product.user_by = product.user_by                    

        existing_product.updatee_date = datetime.datetime.now()
        db.session().commit()
        db.session.refresh(existing_product)

    @staticmethod
    def get_by_id(id):
        return Product.query.filter_by(id=id).first()

    @staticmethod
    def get_all_by_vendor(vendor_id):
        return Product.query.filter_by(id=vendor_id).order_by(Product.product_name).all()

    @staticmethod
    def delete(id):
        db.session.delete(ProductDao.get_by_id(id))
        db.session.commit()
