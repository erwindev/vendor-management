from app import db
from app.vendor.models.product import Product, ProductAttachment, ProductNote


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


class ProductAttachmentDao:

    @staticmethod
    def save_product_attachment(product_attachment):
        db.session.add(product_attachment)
        db.session.commit()
        db.session.refresh(product_attachment)
        return product_attachment

    @staticmethod
    def get_by_id(id):
        return ProductAttachment.filter_by(id=id).first()

    @staticmethod
    def get_by_product_id(software_id):
        return ProductAttachment.filter_by(product_id=software_id)

    @staticmethod
    def delete(id):
        db.session.delete(ProductAttachmentDao.get_by_id(id))
        db.session.commit()


class ProductNoteDao:

    @staticmethod
    def save_product_note(product_note):
        db.session.add(product_note)
        db.session.commit()
        db.session.refresh(product_note)
        return product_note

    @staticmethod
    def get_by_id(id):
        return ProductNote.filter_by(id=id).first()

    @staticmethod
    def get_by_product_id(product_id):
        return ProductNote.filter_by(product_id=product_id)

    @staticmethod
    def delete(id):
        db.session.delete(ProductNoteDao.get_by_id(id))
        db.session.commit()
