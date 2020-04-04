
from app import db
from app.vendor.models.attachment import Attachment

class AttachmentDao:

    @staticmethod
    def save_attachment(attachment):
        db.session.add(attachment)
        db.session.commit()
        db.session.refresh(attachment)
        return attachment

    @staticmethod
    def get_by_id(attachment_id, attachment_type_id):
        return Attachment.query.filter_by(attachment_id=attachment_id, attachment_type_id=attachment_type_id).first()

    @staticmethod
    def get_all_by_type(attachment_type_id):
        return Attachment.query.filter_by(attachment_type_id=attachment_type_id)   
