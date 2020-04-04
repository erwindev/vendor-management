from app import db
from datetime import datetime


class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    website = db.Column(db.String(100))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime)
    status = db.Column(db.String(3))

    def __repr__(self):
        return '<Vendor {}>'.format(self.name)

    def to_json(self):
        json_result = {
            'id': self.id,
            'name': self.name,
            'website': self.website,
            'create_date': self.create_date
        }
        return json_result                