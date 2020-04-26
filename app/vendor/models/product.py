from app import db
from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    product_name = db.Column(db.String(80))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime)
    status = db.Column(db.String(10))
    user_by = db.Column(db.String(100))

    def __repr__(self):
        return '<Product {}>'.format(self.product_name)

    def to_json(self):
        json_result = {
            'id': self.id,
            'vendor_id': self.vendor_id,
            'product_name': self.product_name,
            'create_date': self.create_date,            
            'updated_date': self.updated_date,
            'user_by': self.user_by
        }
        return json_result                
