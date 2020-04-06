import datetime
from app import db
from app.vendor.models.user import User, BlackListToken


class UserDao:
    @staticmethod
    def save_user(user):
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user

    @staticmethod
    def update_user(user):
        existing_user = UserDao.get_by_id(user.id)
        if user.firstname:
            existing_user.fistname = user.firstname
        
        if user.lastname:
            existing_user.lastname = user.lastname

        if user.status:
            existing_user.status = user.status
            
        existing_user.updated_date = datetime.datetime.now()
        db.session.commit()
        db.session.refresh(existing_user)
        return existing_user   

    @staticmethod
    def set_last_login_date(id):
        existing_user = User.query.filter_by(id=id).first()
        existing_user.last_login_date = datetime.datetime.now()
        db.session.commit()
        db.session.refresh(existing_user)
        return existing_user   

    @staticmethod
    def get_by_id(id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_email(email_data):
        return User.query.filter_by(email=email_data).first()


class BlackListTokenDao:

    @staticmethod
    def save_token(token):
        blacklist_token = BlackListToken(token=token)
        db.session.add(blacklist_token)
        db.session.commit()
        db.session.refresh(blacklist_token)
        return blacklist_token
        
