from app import db
from datetime import datetime


##
# Address Type ID (address_type_id)
#   1000 = vendor
#   1001 = contact
##
class Address(db.Model):
    address_id = db.Column(db.Integer, primary_key=True)
    address_type_id = db.Column(db.Integer, primary_key=True)
    street1 = db.Column(db.String(100))
    street2 = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    zipcode = db.Column(db.String(15))

    def __repr__(self):
        return '<Address: {} {} {}>'.format(
            self.address_id,
            self.address_type_id,
            self.street1,
            self.street2,
            self.city,
            self.state,
            self.country,
            self.zipcode
        )

    def to_json(self):
        json_data = {
            'address_id': self.address_id,
            'address_type_id': self.address_type_id,
            'street1': self.street1,
            'street2': self.street2,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'zipcode': self.zipcode
        }
        return json_data
