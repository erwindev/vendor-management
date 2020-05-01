import sys
from flask import jsonify, request
from flask_restplus import Api, Resource, Namespace, fields
from app.vendor.dao.vendor import VendorDao
from app.vendor.dao.contact import ContactDao
from app.vendor.dao.product import ProductDao
from app.vendor.dao.notes import NotesDao
from app.vendor.dao.attachment import AttachmentDao
from app.vendor.models.vendor import Vendor as VendorModel
from app.vendor.util.decorator import token_required
from app.vendor.api.product import ProductDto
from app.vendor.api.contact import ContactDto
from app.vendor.api.notes import NotesDto
from app.vendor.api.attachment import AttachmentDto


class VendorDto:
    api = Namespace('vendor', description='vendor related operations')
    vendor = api.model('vendor', {
        'id': fields.String(),
        'name': fields.String(required=True),
        'status': fields.String(required=True),
        'create_date': fields.Date(),
        'updated_date': fields.Date(),
        'user_by': fields.String(required=True)        
    })      
    message = api.model('message', {
        'status': fields.String(required=True),
        'message': fields.String(required=True),
    })      
    resultlist =  api.model('resultlist', {
        'vendor': fields.Nested(vendor),
        'contacts': fields.List(fields.Nested(ContactDto.contact)),
        'products': fields.List(fields.Nested(ProductDto.product)),
        'notes': fields.List(fields.Nested(NotesDto.notes)),
        'attachments': fields.List(fields.Nested(AttachmentDto.attachment)),
        'result': fields.Nested(message)
    })      
    active_vendor = api.model('active_vendor', {
        'id': fields.String(),
        'name': fields.String(required=True)
    })       


api = VendorDto.api

@api.route('')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class VendorList(Resource):

    @api.doc('list_of_vendor')
    @api.marshal_list_with(VendorDto.vendor, envelope='vendorlist')
    @token_required
    def get(self):
        """ Get all vendors """
        try:
            vendorlist = VendorDao.get_all()
            vendor_ret_list = []
            for vendor in vendorlist:
                vendor_ret_list.append(vendor.to_json())
            return vendor_ret_list
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500

    @api.response(201, 'Vendor successfully created.')
    @api.doc('create a new vendor')
    @api.expect(VendorDto.vendor, validate=True)
    @token_required
    def post(self):
        """Insert a vendor"""
        try:
            vendor_data = request.json

            new_vendor = VendorModel()
            new_vendor.name = vendor_data['name']
            new_vendor.status = vendor_data['status']
            new_vendor.user_by = vendor_data['user_by']
            new_vendor = VendorDao.save_vendor(new_vendor)
            response_object = {
                'status': 'success',
                'message': 'Vendor successfully added.'
            }
            return response_object, 201
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500

    @api.response(201, 'Vendor successfully updated.')
    @api.doc('update a new vendor')
    @api.expect(VendorDto.vendor, validate=False)
    @token_required
    def put(self):
        """Update a vendor"""
        try:
            vendor_data = request.json

            existing_vendor = VendorModel()
            existing_vendor.id = vendor_data['id']
            
            if 'name' in vendor_data:
                existing_vendor.name = vendor_data['name']

            if 'status' in vendor_data:
                existing_vendor.status = vendor_data['status']

            if 'user_by' in vendor_data:
                existing_vendor.user_by = vendor_data['user_by']                    

            existing_vendor = VendorDao.update_vendor(existing_vendor)
            response_object = {
                'status': 'success',
                'message': 'Vendor successfully updated.'
            }
            return response_object, 201
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500


@api.route("/active")
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class VendorActiveList(Resource):

    @api.doc('list_of_active_vendor')
    @api.marshal_list_with(VendorDto.active_vendor, envelope='active_vendors')
    @token_required
    def get(self):
        """ Get all active vendors """
        try:
            vendorlist = VendorDao.get_by_status('Active')
            vendor_ret_list = []
            for vendor in vendorlist:
                vendor_ret_list.append(vendor.to_json())
            return vendor_ret_list
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500


@api.route('/<id>')
@api.param('id', 'The Vendor identifier')
@api.response(404, 'Vendor not found.')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class Vendor(Resource):

    @api.doc('get a vendor')
    @api.marshal_with(VendorDto.resultlist, code=200, description='Successful')
    @token_required
    def get(self, id):
        """Get a vendor given its identifier"""
        vendor = VendorDao.get_by_id(id)
        if not vendor:
            response_object = {
                'status': 'fail',
                'message': 'Vendor not found.'
            }
            return response_object, 404
        else:
            vendor_type_id = 1000
            'Get Contacts'
            contacts = ContactDao.get_contacts(vendor.id, vendor_type_id)
            'Get Products'
            products = ProductDao.get_all_by_vendor(vendor.id)
            'Get Notes'
            notes = NotesDao.get_notes(vendor.id, vendor_type_id)
            'Get Attachments'
            attachments = AttachmentDao.get_attachment(vendor.id, vendor_type_id)
            result = {
                'status': 'success',
                'message': 'Vendor found.'
            }            
            response_object = {
                'vendor': vendor,
                'contacts': contacts,
                'products': products,
                'notes': notes,
                'attachments': attachments,
                'result': result
            }
            return response_object, 200


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
