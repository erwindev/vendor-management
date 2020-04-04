from app import db
from datetime import datetime


class Software(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    software_name = db.Column(db.String(80))
    provider = db.Column(db.String(80))
    department = db.Column(db.String(80))
    budget_owner = db.Column(db.String(80))
    software_owner = db.Column(db.String(80))
    expiration_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(80))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_update_date = db.Column(db.DateTime)
    notes = db.relationship('SoftwareNote', backref="software", cascade="all, delete-orphan", lazy='dynamic')
    attachments = db.relationship('SoftwareAttachment', backref="software", cascade="all, delete-orphan", lazy='dynamic')

    def __repr__(self):
        return '<Software {}>'.format(self.software_name)

    def to_json(self):
        json_result = {
            'id': self.id,
            'software_name': self.software_name,
            'provider': self.provider,
            'department': self.department,
            'budget_owner': self.budget_owner,
            'software_owner': self.software_owner,
            'expiration_date': self.expiration_date,
            'payment_method': self.payment_method,
            'create_date': self.create_date,            
            'last_update_date': self.last_update_date
        }
        return json_result                


class SoftwareAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    software_id = db.Column(db.Integer, db.ForeignKey('software.id'))
    name = db.Column(db.String(100))
    description = db.Column(db.String(2000))
    link = db.Column(db.String(1000))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<SoftwareAttachment {}>'.format(self.name)


class SoftwareNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    software_id = db.Column(db.Integer, db.ForeignKey('software.id'))
    note = db.Column(db.String(2000))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<SoftwareAttachment {}>'.format(self.name)