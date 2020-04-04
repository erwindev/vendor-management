from app import db
from datetime import datetime


class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    website = db.Column(db.String(100))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Vendor {}>'.format(self.name)
