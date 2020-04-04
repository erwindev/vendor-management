from app import db
from app.vendor.models.vendor import Vendor


class VendorDao:

    @staticmethod
    def save_vendor(vendor):
        db.session.add(vendor)
        db.session.commit()
        db.session.refresh(vendor)
        return vendor

    @staticmethod
    def get_by_id(id):
        return Vendor.query.filter_by(id=id).first()

    @staticmethod
    def get_by_name(name):
        return User.query.filter_by(name=name).first()

    @staticmethod
    def get_all():
        return Vendor.query.order_by(Vendor.name).all()
