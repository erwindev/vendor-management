from app import db
from datetime import datetime


##
# Attachment Type ID (attachment_type_id)
#   1000 = vendor
#   1001 = contact
##
class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attachment_id = db.Column(db.Integer)
    attachment_type_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    description = db.Column(db.String(2000))
    link = db.Column(db.String(1000))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime)
    user_by = db.Column(db.String(100))

    def __repr__(self):
        return '<Attachment: {} {} {}>'.format(
            self.id,
            self.attachment_id,
            self.attachment_type_id,
            self.name,
            self.description,
            self.link,
            self.create_date,
            self.update_date,
            self.user_by
        )

    def to_json(self):
        json_data = {
            'id': self.id,
            'attachment_id': self.attachment_id,
            'attachment_type_id': self.attachment_type_id,
            'name': self.name,
            'description': self.description,
            'link': self.link,
            'create_date': self.create_date,
            'update_date': self.update_date,
            'user_by': self.user_by
        }
        return json_data

