
import datetime
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
    def update_attachment(attachment):
        existing_attachment = AttachmentDao.get_by_id(attachment.id)

        if attachment.name:
            existing_attachment.name = attachment.name

        if attachment.link:
            existing_attachment.link = attachment.link

        if attachment.description:
            existing_attachment.description = attachment.description

        if attachment.user_by:
            existing_attachment.user_by = attachment.user_by            

        existing_attachment.update_date = datetime.datetime.now()  
        db.session.commit()
        db.session.refresh(existing_attachment)

        return existing_attachment        

    @staticmethod
    def get_attachment(attachment_id, attachment_type_id):
        return Attachment.query.filter_by(attachment_id=attachment_id, attachment_type_id=attachment_type_id)

    @staticmethod
    def get_by_id(id):
        return Attachment.query.filter_by(id=id).first()   

    @staticmethod
    def delete(id):
        attachment = AttachmentDao.get_by_id(id)
        db.session.delete(attachment)
        db.session.commit()                
