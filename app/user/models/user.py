from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
    status = db.Column(db.String(10))

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        return {
            'id': str(self.id),
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'create_date': self.create_date.isoformat() if self.create_date else None,
            'last_login_date': self.last_login_date.isoformat() if self.last_login_date else None,
            'updated_date': self.updated_date.isoformat() if self.updated_date else None,
            'status': self.status
        }


class BlackListToken(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<BlackListToken {}>'.format(self.token)

    @staticmethod
    def check(auth_token):
        
        if BlackListToken.query.filter_by(token=str(auth_token)).first():
            return True
        else:
            return False
    
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

