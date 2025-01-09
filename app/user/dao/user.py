import datetime
from typing import Optional, List
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.user.models.user import User, BlackListToken


class UserDao:
    @staticmethod
    def _commit_and_refresh(instance) -> Optional[object]:
        """Helper method to handle common commit and refresh operations"""
        try:
            db.session.commit()
            db.session.refresh(instance)
            return instance
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def save_user(user: User) -> Optional[User]:
        try:
            db.session.add(user)
            return UserDao._commit_and_refresh(user)
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def update_user(user: User) -> Optional[User]:
        existing_user = UserDao.get_by_id(user.id)
        if not existing_user:
            return None

        # Update fields using dictionary comprehension
        update_fields = {
            'firstname': user.firstname,
            'lastname': user.lastname,
            'password_hash': user.password_hash,
            'status': user.status
        }
        
        # Only update non-None values
        for field, value in update_fields.items():
            if value is not None:
                setattr(existing_user, field, value)
        
        existing_user.updated_date = datetime.datetime.now()
        return UserDao._commit_and_refresh(existing_user)

    @staticmethod
    def change_password(id: int, new_password: str) -> Optional[User]:
        user = UserDao.get_by_id(id)
        if not user:
            return None
            
        user.set_password(new_password)
        user.updated_date = datetime.datetime.now()
        return UserDao._commit_and_refresh(user)

    @staticmethod
    def set_last_login_date(id: int) -> Optional[User]:
        user = UserDao.get_by_id(id)
        if not user:
            return None
            
        user.last_login_date = datetime.datetime.now()
        return UserDao._commit_and_refresh(user)

    @staticmethod
    def get_by_id(id: int) -> Optional[User]:
        return User.query.filter_by(id=id).first()

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_all() -> List[User]:
        return User.query.all()


class BlackListTokenDao:
    @staticmethod
    def save_token(token: str) -> Optional[BlackListToken]:
        blacklist_token = BlackListToken(token=token)
        try:
            db.session.add(blacklist_token)
            return UserDao._commit_and_refresh(blacklist_token)
        except SQLAlchemyError:
            db.session.rollback()
            raise
        
