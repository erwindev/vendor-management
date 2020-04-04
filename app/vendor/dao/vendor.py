import datetime
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
    def update_vendor(vendor):
        existing_vendor = Vendor.query.filter_by(id=vendor.id).first()
        existing_vendor.name = vendor.name
        existing_vendor.website = vendor.website
        existing_vendor.status = vendor.status
        existing_vendor.updated_date = datetime.datetime.now()
        db.session.commit()
        db.session.refresh(existing_vendor)
        return existing_vendor

    @staticmethod
    def get_by_id(id):
        return Vendor.query.filter_by(id=id).first()

    @staticmethod
    def get_by_name(name):
        return User.query.filter_by(name=name).first()

    @staticmethod
    def get_all():
        return Vendor.query.order_by(Vendor.name).all()
