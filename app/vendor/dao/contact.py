
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

        if contact.name:
            existing_contact.name = contact.name

        if contact.email:
            existing_contact.email = contact.email

        if contact.phone1:
            existing_contact.phone1 = contact.phone1

        if contact.phone2:
            existing_contact.phone2 = contact.phone2

        if contact.street1:
            existing_contact.street1 = contact.street1

        if contact.street2:
            existing_contact.street2 = contact.street2

        if contact.city:
            existing_contact.city = contact.city

        if contact.state:
            existing_contact.state = contact.state

        if contact.country:
            existing_contact.country = contact.country

        if contact.zipcode:
            existing_contact.zipcode = contact.zipcode

        if contact.status:
            existing_contact.status = contact.status
            
        existing_contact.update_date = datetime.datetime.now()  
        db.session.commit()
        db.session.refresh(existing_contact)
        return existing_contact        

    @staticmethod
    def get_by_id(contact_id, contact_type_id):
        return Contact.query.filter_by(contact_id=contact_id, contact_type_id=contact_type_id).first()
