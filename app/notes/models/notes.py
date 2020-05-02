from app import db
from datetime import datetime


##
# Notes Type ID (notes_type_id)
#   1000 = vendor
#   1001 = product
##
class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes_id = db.Column(db.Integer)
    notes_type_id = db.Column(db.Integer)
    notes = db.Column(db.String(2000))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_by = db.Column(db.String(100))

    def __repr__(self):
        return '<Notes: {} {} {}>'.format(
            self.id,
            self.notes_id,
            self.notes_type_id,
            self.notes,
            self.create_date,
            self.user_by
        )

    def to_json(self):
        json_data = {
            'id': self.id,
            'notes_id': self.notes_id,
            'notes_type_id': self.notes_type_id,
            'notes': self.notes,
            'create_date': self.create_date,
            'update_date': self.update_date,
            'user_by': self.user_by
        }
        return json_data
