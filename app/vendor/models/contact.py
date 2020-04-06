from app import db
from datetime import datetime

##
# Contact Type ID (contact_type_id)
#   1000 = vendor
#   1001 = product
##

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer)
    contact_type_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone1 = db.Column(db.String(100))
    phone2 = db.Column(db.String(100))
    street1 = db.Column(db.String(100))
    street2 = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    zipcode = db.Column(db.String(15))    
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime)
    status = db.Column(db.String(3))
    user_by = db.Column(db.String(100))

    def __repr__(self):
        return '<Contact: {} {} {}>'.format(
            self.id,
            self.contact_id,
            self.contact_type_id,
            self.name,
            self.email,
            self.phone1,
            self.phone2,
            self.street1,
            self.street2,
            self.city,
            self.state,
            self.country,
            self.zipcode,            
            self.create_date,
            self.updated_date,
            self.status,
            self.user_by
        )

    def to_json(self):
        json_data = {
            'id': self.id,            
            'contact_id': self.contact_id,
            'contact_type_id': self.contact_type_id,
            'name': self.name,
            'street2': self.street2,
            'email': self.email,
            'phone1': self.phone1,
            'street1': self.street1,
            'street2': self.street2,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'zipcode': self.zipcode,            
            'create_date': self.create_date,
            'updated_date': self.updated_date,
            'status': self.status,
            'user_by': self.user_by                
        }
        return json_data


    VENDOR_TYPE_ID = 1000
    PRODUCT_TYPE_ID = 1001