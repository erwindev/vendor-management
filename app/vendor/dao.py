from app import db
from app.vendor.models import User, Software, SoftwareAttachment, SoftwareNote
from sqlalchemy.exc import OperationalError


class UserDao:
    @staticmethod
    def save_user(user):
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user

    @staticmethod
    def get_by_id(self, id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_all():
        return User.query.all()


class SoftwareDao:
    @staticmethod
    def save_software(software):
        db.session.add(software)
        db.session.commit()
        return software

    @staticmethod
    def get_by_id(id):
        return Software.query.filter_by(id=id).first()

    @staticmethod
    def get_all():
        return Software.query.order_by(Software.software_name).all()

    @staticmethod
    def get_software_pagination(sort_order=Software.software_name):
        return Software.query.order_by(sort_order)

    @staticmethod
    def delete(id):
        db.session.delete(SoftwareDao.get_by_id(id))
        db.session.commit()


class SoftwareAttachmentDao:
    @staticmethod
    def save_software_attachment(software_attachment):
        db.session.add(software_attachment)
        db.session.commit()
        return software_attachment

    @staticmethod
    def get_by_id(id):
        return SoftwareAttachment.filter_by(id=id).first()

    @staticmethod
    def get_all():
        return SoftwareAttachment.order_by(SoftwareAttachment.create_date)

    @staticmethod
    def delete(id):
        db.session.delete(SoftwareAttachment.get_by_id(id))
        db.session.commit()


class SoftwareNoteDao:
    @staticmethod
    def save_software_note(software_note):
        db.session.add(software_note)
        db.session.commit()
        return software_note

    @staticmethod
    def get_by_id(id):
        return SoftwareNote.filter_by(id=id).first()

    @staticmethod
    def get_all():
        return SoftwareNote.order_by(SoftwareNote.create_date)

    @staticmethod
    def delete(id):
        db.session.delete(SoftwareNote.get_by_id(id))
        db.session.commit()
