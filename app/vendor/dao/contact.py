
import datetime
from app import db
from app.vendor.models.contact import Contact

class ContactDao:
    @staticmethod
    def save_contact(contact):
        db.session.add(contact)
        db.session.commit()
        db.session.refresh(contact)
        return contact

    @staticmethod
    def update_contact(contact):
        existing_contact = get_by_id(contact.contact_id, contact.contact_type_id)
        existing_contact.name = contact.name
        existing_contact.email = contact.email
        existing_contact.phone1 = contact.phone1
        existing_contact.phone2 = contact.phone2
        existing_contact.street1 = contact.street1
        existing_contact.street2 = contact.street2
        existing_contact.city = contact.city
        existing_contact.state = contact.state
        existing_contact.country = contact.country
        existing_contact.zipcode = contact.zipcode
        existing_contact.status = contact.status
        existing_contact.update_date = datetime.datetime.now()  
        db.session.commit()
        db.session.refresh(existing_contact)
        return existing_contact        

    @staticmethod
    def get_by_id(contact_id, contact_type_id):
        return Contact.query.filter_by(contact_id=contact_id, contact_type_id=contact_type_id).first()

    @staticmethod
    def get_all_by_type(contact_type_id):
        return Contact.query.filter_by(contact_type_id=contact_type_id)           
