import sys
from flask import jsonify, request
from flask_restplus import Api, Resource, Namespace, fields
from app.vendor.dao.software import SoftwareDao, SoftwareAttachmentDao, SoftwareNoteDao
from app.vendor.models.software import Software as SoftwareModel
from app.vendor.models.software import SoftwareAttachment as SoftwareAttachmentModel
from app.vendor.models.software import SoftwareNote as SoftwareNoteModel
from app.vendor.util.decorator import token_required


class SoftwareDto:
    api = Namespace('software', description='software related operations')
    software = api.model('software', {
        'id': fields.String(),
        'software_name': fields.String(required=True),
        'provider': fields.String(required=True),
        'department': fields.String(required=True),
        'budget_owner': fields.String(required=True),
        'software_owner': fields.String(required=True),
        'expiration_date': fields.String(required=True),
        'payment_method': fields.String(required=True),
        'create_date': fields.DateTime(required=True),
        'last_update_date': fields.DateTime(required=True)    
    })
    software_attachment = api.model('software_attachment', {
        'id': fields.String(),
        'software_id': fields.String(required=True),
        'name': fields.String(required=True),
        'description': fields.String(required=True),
        'link': fields.String(required=True),
        'create_date': fields.DateTime(required=True)   
    })
    software_note = api.model('software_note', {
        'id': fields.String(),
        'software_id': fields.String(required=True),
        'note': fields.String(required=True),
        'create_date': fields.DateTime(required=True)   
    })               


api = SoftwareDto.api

@api.route("/")
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class SoftwareList(Resource):

    @api.doc('list_of_software')
    @api.marshal_list_with(SoftwareDto.software, envelope='softwarelist')
    @token_required
    def get(self):
        """Get all software"""
        try:
            sofwares = SoftwareDao.get_all()
            software_ret_list = []
            for software in sofwares:
                software_ret_list.append(software.to_json())
            return software_ret_list
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500    


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

