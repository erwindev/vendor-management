
import datetime
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
    def update_notes(notes):
        existing_notes = NotesDao.get_by_id(notes.id)

        if notes.notes:
            existing_notes.notes = notes.notes

        if notes.user_by:
            existing_notes.user_by = notes.user_by            

        existing_notes.update_date = datetime.datetime.now()  
        db.session.commit()
        db.session.refresh(existing_notes)

        return existing_notes

    @staticmethod
    def get_notes(notes_id, notes_type_id):
        return Notes.query.filter_by(notes_id=notes_id, notes_type_id=notes_type_id)

    @staticmethod
    def get_by_id(id):
        return Notes.query.filter_by(id=id).first()

    @staticmethod
    def delete(id):
        notes = Notes.query.filter_by(id=id).first()
        db.session.delete(notes)
        db.session.commit()        
