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
    def get_by_id(id):
        return Product.query.filter_by(id=id).first()

    @staticmethod
    def get_all():
        return Product.query.order_by(Product.product_name).all()

    @staticmethod
    def delete(id):
        db.session.delete(ProductDao.get_by_id(id))
        db.session.commit()
