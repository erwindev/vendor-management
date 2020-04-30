import sys
from flask import jsonify, request
from flask_restplus import Api, Resource, Namespace, fields
from app.vendor.dao.notes import NotesDao
from app.vendor.models.notes import Notes as NotesModel
from app.vendor.util.decorator import token_required


class NotesDto:
    api = Namespace('notes', description='notes related operations')
    notes = api.model('notes', {
        'id': fields.String(),
        'notes_id': fields.String(required=True),
        'notes_type_id': fields.String(required=True),        
        'notes': fields.String(required=True),
        'create_date': fields.DateTime(),   
        'updated_date': fields.DateTime(),
        'user_by': fields.String(required=True)  
    })            


api = NotesDto.api

@api.route('/<notes_id>/<notes_type_id>')
@api.response(404, 'Notes not found.')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class NotesList(Resource):

    @api.doc('get all notes associated to an notes_id')
    @api.marshal_list_with(NotesDto.notes, envelope='noteslist')
    @token_required
    def get(self, notes_id, notes_type_id):
        """Get notes based on the given identifier"""
        notes = NotesDao.get_notes(notes_id, notes_type_id)
        if not notes:
            response_object = {
                'status': 'fail',
                'message': 'No data found.'
            }
            return response_object, 404
        else:
            note_ret_list = []
            for note in notes:
                note_ret_list.append(note.to_json())
            return note_ret_list


@api.route('')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class AddNotes(Resource):

    @api.response(201, 'Note successfully created.')
    @api.doc('create a new note')
    @api.expect(NotesDto.notes, validate=True)
    @token_required
    def post(self):
        """Insert a new notes"""
        try:
            notes_data = request.json
            
            new_notes = NotesModel()
            new_notes.notes_id = notes_data['notes_id']
            new_notes.notes_type_id = notes_data['notes_type_id']
            new_notes.notes = notes_data['notes']
            new_notes.user_by = notes_data['user_by']
            new_notes = NotesDao.save_notes(new_notes)
            response_object = {
                'status': 'success',
                'message': 'Notes successfully added.'
            }
            return response_object, 201
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500


@api.route('/<id>')
@api.param('id', 'The Notes identifier')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class Notes(Resource):

    @api.response(201, 'Notes successfully updated.')
    @api.doc('update a notes')
    @api.expect(NotesDto.notes, validate=False)
    @token_required
    def put(self, id):
        """Update a notes"""
        try:
            notes_data = request.json
            existing_notes = NotesDao.get_by_id(id)            

            if 'notes_id' in notes_data:
                existing_notes.notes_id = notes_data['notes_id']

            if 'notes_type_id' in notes_data:
                existing_notes.notes_type_id = notes_data['notes_type_id']

            if 'notes' in notes_data:
                existing_notes.notes = notes_data['notes']

            if 'user_by' in notes_data:
                existing_notes.user_by = notes_data['user_by']                 

            existing_notes = NotesDao.update_notes(existing_notes)
            response_object = {
                'status': 'success',
                'message': 'Notes successfully updated.'
            }
            return response_object, 201
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500


    @api.doc('get a notes')
    @api.marshal_with(NotesDto.notes)
    @token_required
    def get(self, id):
        """Get a notes given its identifier"""
        notes = NotesDao.get_by_id(id)  
        if not notes:
            response_object = {
                'status': 'fail',
                'message': 'Notes not found.'
            }
            return response_object, 404
        else:
            return notes

    @api.doc('delete a notes')
    @token_required
    def delete(self, id):
        """Delete a notes given its identifier"""
        NotesDao.delete(id)  
        response_object = {
            'status': 'success',
            'message': 'Notes deleted.'
        }
        return response_object, 202

@api.errorhandler(Exception)
def generic_exception_handler(e: Exception):
    exc_type, exc_value, exc_traceback = sys.exc_info()

    if exc_traceback:
        traceback_details = {
            'filename': exc_traceback.tb_frame.f_code.co_filename,
            'lineno': exc_traceback.tb_lineno,
            'name': exc_traceback.tb_frame.f_code.co_name,
            'message': str(exc_value),
        }
        return {
            'status': 'error',
            'message': traceback_details['message']
        }, 500
    else:
        return {
            'status': 'error',
            'message': 'Internal Server Error'
        }, 500    
