
from app import db
from app.vendor.models.address import Address

class AddressDao:

    @staticmethod
    def save_address(address):
        db.session.add(address)
        db.session.commit()
        db.session.refresh(address)
        return address

    @staticmethod
    def get_by_id(address_id, address_type_id):
        return Address.query.filter_by(address_id=address_id, address_type_id=address_type_id).first()
