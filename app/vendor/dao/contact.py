
from app import db
from app.vendor.models.contact import Contact

class ContactDao:
    @staticmethod
    def save(contact):
        db.session.add(contact)
        db.session.commit()
        db.session.refresh(contact)
        return contact

    @staticmethod
    def get_by_id(contact_id, contact_type_id):
        return Contact.query.filter_by(contact_id=contact_id, contact_type_id=contact_type_id).first()

    @staticmethod
    def get_all_by_type(contact_type_id):
        return Contact.query.filter_by(contact_type_id=contact_type_id)           
