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

    def to_json(self):
        json_result = {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'username': self.username,
            'username': self.username,
            'create_date': self.create_date
        }
        return json_result        
