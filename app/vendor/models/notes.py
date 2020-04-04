from app import db
from datetime import datetime


##
# Notes Type ID (notes_type_id)
#   1000 = vendor
#   1001 = product
##
class Notes(db.Model):
    notes_id = db.Column(db.Integer, primary_key=True)
    notes_type_id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(2000))

    def __repr__(self):
        return '<Notes: {} {} {}>'.format(
            self.notes_id,
            self.notes_type_id,
            self.notes
        )

    def to_json(self):
        json_data = {
            'notes_id': self.notes_id,
            'notes_type_id': self.notes_type_id,
            'notes': self.notes
        }
        return json_data
