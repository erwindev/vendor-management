from app import db
from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    product_name = db.Column(db.String(80))
    department = db.Column(db.String(100))
    budget_owner = db.Column(db.String(100))
    product_owner = db.Column(db.String(100))
    expiration_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(100))
    product_type = db.Column(db.String(100))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime)
    status = db.Column(db.String(3))

    def __repr__(self):
        return '<Product {}>'.format(self.product_name)

    def to_json(self):
        json_result = {
            'id': self.id,
            'vendor_id': self.vendor_id,
            'product_name': self.product_name,
            'department': self.department,
            'budget_owner': self.budget_owner,
            'product_owner': self.product_owner,
            'expiration_date': self.expiration_date,
            'payment_method': self.payment_method,
            'product_type': self.product_type,
            'create_date': self.create_date,            
            'updated_date': self.updated_date
        }
        return json_result                
