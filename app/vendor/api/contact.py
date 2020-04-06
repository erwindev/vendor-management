import sys
from flask import jsonify, request
from flask_restplus import Api, Resource, Namespace, fields
from app.vendor.dao.contact import ContactDao
from app.vendor.dao.vendor import VendorDao
from app.vendor.models.contact import Contact as ContactModel
from app.vendor.util.decorator import token_required


class ContactDto:
    api = Namespace('contact', description='contact related operations')
    contact = api.model('contact', {
        'contact_id': fields.String(),
        'contact_type_id': fields.String(),        
        'name': fields.String(required=True),
        'email': fields.String(required=True),        
        'phone1': fields.String(required=True),       
        'phone2': fields.String(required=True),         
        'street1': fields.String(required=True),                        
        'street2': fields.String(required=True),  
        'city': fields.String(required=True),  
        'state': fields.String(required=True),  
        'country': fields.String(required=True),  
        'zipcode': fields.String(required=True),  
        'create_date': fields.DateTime(),   
        'updated_date': fields.DateTime(),
        'status': fields.String()  
    })            


api = ContactDto.api

@api.route('/<contact_id>/<contact_type_id>')
@api.param('id', 'The Vendor identifier')
@api.response(404, 'Vendor not found.')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class VendorContactList(Resource):

    @api.doc('get all vendor contacts')
    @api.marshal_with(ContactDto.contact)
    @token_required
    def get(self, contact_id, contact_type_id):
        """Get contacts for vendor given its identifier"""
        vendor = VendorDao.get_by_id(contact_id)
        if not vendor:
            response_object = {
                'status': 'fail',
                'message': 'Vendor not found.'
            }
            return response_object, 404
        else:
            contacts = ContactDao.get_by_id(contact_id, contact_type_id)
            contact_ret_list = []
            for contact in contacts:
                contact_ret_list.append(contact.to_json())
            return contact_ret_list


    @api.response(201, 'Vendor contact successfully created.')
    @api.doc('create a new vendor contact')
    @api.expect(ContactDto.contact, validate=True)
    @token_required
    def post(self, contact_id, contact_type_id):
        """Insert a vendor contact"""
        try:
            vendor = VendorDao.get_by_id(id)            
            contact_data = request.json

            new_contact = ContactModel()
            if 'name' in contact_data:
                new_contact.name = contact_data['name']

            if 'email' in contact_data:
                new_contact.email = contact_data['email']

            if 'phone1' in contact_data:
                new_contact.phone1 = contact_data['phone1']

            if 'phone2' in contact_data:
                new_contact.phone2 = contact_data['phone2']

            if 'street1' in contact_data:
                new_contact.street1 = contact_data['street1']

            if 'street2' in contact_data:
                new_contact.street2 = contact_data['street2']

            if 'city' in contact_data:
                new_contact.city = contact_data['city']

            if 'state' in contact_data:
                new_contact.state = contact_data['state']

            if 'country' in contact_data:
                new_contact.country = contact_data['country']

            if 'zipcode' in contact_data:
                new_contact.zipcode = contact_data['zipcode']

            new_contact.contact_id = vendor.id
            new_contact.contact_type_id = contact_type_id

            new_contact = ContactDao.save_contact(new_contact)
            response_object = {
                'status': 'success',
                'message': 'Vendor contact successfully added.'
            }
            return response_object, 201
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
