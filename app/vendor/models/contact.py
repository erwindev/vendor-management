from app import db
from datetime import datetime

##
# Contact Type ID (contact_type_id)
#   1000 = vendor
#   1001 = product
##
class Contact(db.Model):
    contact_id = db.Column(db.Integer, primary_key=True)
    contact_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone1 = db.Column(db.String(100))
    phone2 = db.Column(db.String(100))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Contact: {} {} {}>'.format(
            self.contact_id,
            self.contact_type_id,
            self.name,
            self.email,
            self.phone1,
            self.phone2,
            self.create_date
        )

    def to_json(self):
        json_data = {
            'contact_id': self.contact_id,
            'contact_type_id': self.contact_type_id,
            'name': self.name,
            'street2': self.street2,
            'email': self.email,
            'phone1': self.phone1,
            'create_date': self.create_date
        }
        return json_data
