from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class TempTable(db.Model):
    __tablename__ = 'temp_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Temp Table: {} {} {}>'.format(
            self.id,
            self.name,
            self.create_date
        )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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
