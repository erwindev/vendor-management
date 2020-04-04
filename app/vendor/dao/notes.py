
from app import db
from app.vendor.models.notes import Notes

class NotesDao:

    @staticmethod
    def save_notes(notes):
        db.session.add(notes)
        db.session.commit()
        db.session.refresh(notes)
        return notes

    @staticmethod
    def get_by_id(notes_id, notes_type_id):
        return Notes.query.filter_by(notes_id=notes_id, notes_type_id=notes_type_id).first()

    @staticmethod
    def get_all_by_type(notes_type_id):
        return Notes.query.filter_by(notes_type_id=notes_type_id)   
