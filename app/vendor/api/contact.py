import sys
from flask import jsonify, request
from flask_restplus import Api, Resource, Namespace, fields
from app.vendor.dao.contact import ContactDao
from app.vendor.models.contact import Contact as ContactModel
from app.vendor.util.decorator import token_required
from app.vendor.util import NullableString


class ContactDto:
    api = Namespace('contact', description='contact related operations')
    contact = api.model('contact', {
        'id': fields.String(),
        'contact_id': fields.String(required=True),
        'contact_type_id': fields.String(required=True),        
        'name': fields.String(required=True),
        'email': fields.String(required=True),        
        'phone1': fields.String(required=True),       
        'phone2': NullableString(),         
        'street1': fields.String(required=True),                        
        'street2': NullableString(),  
        'city': fields.String(required=True),  
        'state': fields.String(required=True),  
        'country': fields.String(required=True),  
        'zipcode': fields.String(required=True),  
        'create_date': fields.DateTime(),   
        'updated_date': fields.DateTime(),
        'status': fields.String(),
        'user_by': fields.String(required=True)   
    })            


api = ContactDto.api

@api.route('/<contact_id>/<contact_type_id>')
@api.response(404, 'Contact not found.')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class ContactList(Resource):

    @api.doc('get all contacts per contact_id')
    @api.marshal_list_with(ContactDto.contact, envelope='contactlist')
    @token_required
    def get(self, contact_id, contact_type_id):
        """Get contacts based on the given identifier"""
        contacts = ContactDao.get_contacts(contact_id, contact_type_id)
        if not contacts:
            response_object = {
                'status': 'fail',
                'message': 'No data found.'
            }
            return response_object, 404
        else:
            contact_ret_list = []
            for contact in contacts:
                contact_ret_list.append(contact.to_json())
            return contact_ret_list, 200


@api.route('')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class AddContact(Resource):

    @api.response(201, 'Contact successfully created.')
    @api.doc('create a new contact')
    @api.expect(ContactDto.contact, validate=True)
    @token_required
    def post(self):
        """Insert a new contact"""
        try:
            contact_data = request.json
            
            new_contact = ContactModel()
            new_contact.contact_id = contact_data['contact_id']
            new_contact.contact_type_id = contact_data['contact_type_id']
            new_contact.name = contact_data['name']
            new_contact.email = contact_data['email']
            new_contact.phone1 = contact_data['phone1']
            new_contact.phone2 = contact_data['phone2']
            new_contact.street1 = contact_data['street1']

            if 'street2' in contact_data:
                new_contact.street2 = contact_data['street2']

            new_contact.city = contact_data['city']
            new_contact.state = contact_data['state']
            new_contact.country = contact_data['country']
            new_contact.zipcode = contact_data['zipcode']
            new_contact.user_by = contact_data['user_by']
            new_contact.status = contact_data['status']

            new_contact = ContactDao.save_contact(new_contact)
            response_object = {
                'status': 'success',
                'message': 'Contact successfully added.'
            }
            return response_object, 201
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500
            

    @api.response(200, 'Contact successfully updated.')
    @api.doc('update a contact')
    @api.expect(ContactDto.contact, validate=False)
    @token_required
    def put(self):
        """Update a contact"""
        try:
            contact_data = request.json
            existing_contact = ContactDao.get_by_id(contact_data['id'])            

            if 'contact_id' in contact_data:
                existing_contact.contact_id = contact_data['contact_id']

            if 'contact_type_id' in contact_data:
                existing_contact.contact_type_id = contact_data['contact_type_id']

            if 'name' in contact_data:
                existing_contact.name = contact_data['name']

            if 'email' in contact_data:
                existing_contact.email = contact_data['email']

            if 'phone1' in contact_data:
                existing_contact.phone1 = contact_data['phone1']

            if 'phone2' in contact_data:
                existing_contact.phone2 = contact_data['phone2']

            if 'street1' in contact_data:
                existing_contact.street1 = contact_data['street1']

            if 'street2' in contact_data:
                existing_contact.street2 = contact_data['street2']

            if 'city' in contact_data:
                existing_contact.city = contact_data['city']

            if 'state' in contact_data:
                existing_contact.state = contact_data['state']

            if 'country' in contact_data:
                existing_contact.country = contact_data['country']

            if 'zipcode' in contact_data:
                existing_contact.zipcode = contact_data['zipcode']

            if 'user_by' in contact_data:
                existing_contact.user_by = contact_data['user_by']                

            if 'status' in contact_data:
                existing_contact.status = contact_data['status']                      

            existing_contact = ContactDao.update_contact(existing_contact)
            response_object = {
                'status': 'success',
                'message': 'Contact successfully updated.'
            }

            return response_object, 200
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500

@api.route('/<id>')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class Contact(Resource):

    @api.doc('get a contact')
    @api.marshal_with(ContactDto.contact)
    @token_required
    def get(self, id):
        """Get a contact given its identifier"""
        contact = ContactDao.get_by_id(id)  
        if not contact:
            response_object = {
                'status': 'fail',
                'message': 'Contact not found.'
            }
            return response_object, 404
        else:
            return contact, 200

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
