from app import db
from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80))
    provider = db.Column(db.String(100))
    department = db.Column(db.String(100))
    budget_owner = db.Column(db.String(100))
    product_owner = db.Column(db.String(100))
    expiration_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(100))
    product_type = db.Column(db.String(100))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_update_date = db.Column(db.DateTime)
    notes = db.relationship('ProductNote', backref="product", cascade="all, delete-orphan", lazy='dynamic')
    attachments = db.relationship('ProductAttachment', backref="product", cascade="all, delete-orphan", lazy='dynamic')

    def __repr__(self):
        return '<Product {}>'.format(self.product_name)

    def to_json(self):
        json_result = {
            'id': self.id,
            'product_name': self.software_name,
            'provider': self.provider,
            'department': self.department,
            'budget_owner': self.budget_owner,
            'product_owner': self.software_owner,
            'expiration_date': self.expiration_date,
            'payment_method': self.payment_method,
            'product_type': self.product_type,
            'create_date': self.create_date,            
            'last_update_date': self.last_update_date
        }
        return json_result                
