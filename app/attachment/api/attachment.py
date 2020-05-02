import sys
from flask import jsonify, request
from flask_restplus import Api, Resource, Namespace, fields
from app.attachment.dao.attachment import AttachmentDao
from app.attachment.models.attachment import Attachment as AttachmentModel
from app.util.decorator import token_required


class AttachmentDto:
    api = Namespace('attachment', description='attachment related operations')
    attachment_api_fields = {
        'id': fields.String(),
        'attachment_id': fields.String(required=True),
        'attachment_type_id': fields.String(required=True),        
        'name': fields.String(required=True),
        'description': fields.String(required=True),
        'link': fields.String(required=True),
        'create_date': fields.Date(),   
        'update_date': fields.DateTime(),
        'user_by': fields.String(required=True)
    }
    attachment = api.model('attachment', attachment_api_fields)            


api = AttachmentDto.api

@api.route('/<attachment_id>/<attachment_type_id>')
@api.response(404, 'Attachment not found.')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class AttachmentList(Resource):

    @api.doc('get all attachment associated to an attachment_id')
    @api.marshal_list_with(AttachmentDto.attachment, envelope='attachmentlist')
    @token_required
    def get(self, attachment_id, attachment_type_id):
        """Get attachment based on the given identifier"""
        attachment = AttachmentDao.get_attachment(attachment_id, attachment_type_id)
        if not attachment:
            response_object = {
                'status': 'fail',
                'message': 'No data found.'
            }
            return response_object, 404
        else:
            attachment_ret_list = []
            for attachment in attachment:
                attachment_ret_list.append(attachment.to_json())
            return attachment_ret_list, 200


@api.route('')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class AddNotes(Resource):

    @api.response(201, 'Note successfully created.')
    @api.doc('create a new attachment')
    @api.expect(AttachmentDto.attachment, validate=True)
    @token_required
    def post(self):
        """Insert a new attachment"""
        try:
            attachment_data = request.json
            
            new_attachment = AttachmentModel()
            new_attachment.attachment_id = attachment_data['attachment_id']
            new_attachment.attachment_type_id = attachment_data['attachment_type_id']
            new_attachment.name = attachment_data['name']
            new_attachment.link = attachment_data['link']
            new_attachment.description = attachment_data['description']
            new_attachment.user_by = attachment_data['user_by']

            new_attachment = AttachmentDao.save_attachment(new_attachment)
            response_object = {
                'status': 'success',
                'message': 'Attachment successfully added.'
            }
            return response_object, 201
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500


@api.route('/<id>')
@api.param('id', 'The Attachment identifier')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class Attachment(Resource):

    @api.response(200, 'Attachment successfully updated.')
    @api.doc('update a attachment')
    @api.expect(AttachmentDto.attachment, validate=False)
    @token_required
    def put(self, id):
        """Update a attachment"""
        try:
            attachment_data = request.json
            existing_attachment = AttachmentDao.get_by_id(id)            

            if 'attachment_id' in attachment_data:
                existing_attachment.attachment_id = attachment_data['attachment_id']

            if 'attachment_type_id' in attachment_data:
                existing_attachment.attachment_type_id = attachment_data['attachment_type_id']

            if 'name' in attachment_data:
                existing_attachment.name = attachment_data['name']

            if 'description' in attachment_data:
                existing_attachment.description = attachment_data['description']

            if 'link' in attachment_data:
                existing_attachment.link = attachment_data['link']

            if 'user_by' in attachment_data:
                existing_attachment.user_by = attachment_data['user_by']                    

            existing_attachment = AttachmentDao.update_attachment(existing_attachment)
            response_object = {
                'status': 'success',
                'message': 'Attachment successfully updated.'
            }

            return response_object, 200
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500


    @api.doc('get an attachment')
    @api.marshal_with(AttachmentDto.attachment)
    @token_required
    def get(self, id):
        """Get an attachment given its identifier"""
        attachment = AttachmentDao.get_by_id(id)  
        if not attachment:
            response_object = {
                'status': 'fail',
                'message': 'Attachment not found.'
            }
            return response_object, 404
        else:
            return attachment

    @api.doc('delete an attachment')
    @token_required
    def delete(self, id):
        """Delete an attachment given its identifier"""
        AttachmentDao.delete(id)  
        response_object = {
            'status': 'success',
            'message': 'Attachment deleted.'
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
