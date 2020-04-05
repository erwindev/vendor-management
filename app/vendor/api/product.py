import sys
from datetime import datetime
from flask import jsonify, request
from flask_restplus import Api, Resource, Namespace, fields
from app.vendor.dao.product import ProductDao
from app.vendor.models.product import Product as ProductModel
from app.vendor.util.decorator import token_required


class ProductDto:
    api = Namespace('product', description='product related operations')
    product = api.model('product', {
        'id': fields.String(),
        'vednor_id': fields.String(),
        'product_name': fields.String(),
        'department': fields.String(),
        'budget_owner': fields.String(),
        'expiration_date': fields.String(),
        'payment_method': fields.String(),
        'product_type': fields.String(),
        'status': fields.String(),
        'create_date': fields.DateTime(),
        'updated_date': fields.DateTime()      
    })      


api = ProductDto.api

@api.route("/vendor/<vendor_id>")
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class ProductList(Resource):

    @api.doc('list_of_product')
    @api.marshal_list_with(ProductDto.product, envelope='productlist')
    @token_required
    def get(self, vendor_id):
        """ Get all products """
        try:
            productlist = ProductDao.get_all_by_vendor(vendor_id)
            product_ret_list = []
            for product in productlist:
                product_ret_list.append(product.to_json())
            return product_ret_list
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500


    @api.response(201, 'Product successfully created.')
    @api.doc('create a new product')
    @api.expect(ProductDto.product, validate=False)
    @token_required
    def post(self, vendor_id):
        """Insert a product"""
        try:
            product_data = request.json

            new_product = ProductModel()
            new_product.vendor_id = vendor_id
            new_product.product_name = product_data['product_name']
            new_product.department = product_data['department']
            new_product.budget_owner = product_data['budget_owner']
            new_product.product_owner = product_data['product_owner']
            new_product.expiration_date = datetime.strptime(product_data['expiration_date'],"%Y-%m-%d").date()
            new_product.payment_method = product_data['payment_method']
            new_product.product_type = product_data['product_type']
            new_product.status = product_data['status']
            new_product = ProductDao.save_product(new_product)
            response_object = {
                'status': 'success',
                'message': 'Product successfully added.'
            }
            return response_object, 201
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500

    @api.response(201, 'Product successfully updated.')
    @api.doc('update a new product')
    @api.expect(ProductDto.product, validate=False)
    @token_required
    def put(self, vendor_id):
        """Update a product"""
        try:
            product_data = request.json

            existing_product = ProductModel()
            existing_product.id = product_data['id']
            existing_product.vendor_id = product_data['vendor_id']
            existing_product.product_name = product_data['product_name']
            existing_product.department = product_data['department']
            existing_product.budget_owner = product_data['budget_owner']
            existing_product.product_owner = product_data['product_owner']
            new_product.expiration_date = datetime.strptime(product_data['expiration_date'],"%Y-%m-%d").date()
            existing_product.payment_method = product_data['payment_method']
            existing_product.product_type = product_data['product_type']
            existing_product.status = product_data['status']            
            existing_product = ProductDto.update_product(existing_vendor)
            response_object = {
                'status': 'success',
                'message': 'Product successfully updated.'
            }
            return response_object, 201
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500



@api.route('/<id>')
@api.param('id', 'The Product identifier')
@api.response(404, 'Product not found.')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class Product(Resource):

    @api.doc('get a product')
    @api.marshal_with(ProductDto.product)
    @token_required
    def get(self, id):
        """Get a product given its identifier"""
        product = ProductDao.get_by_id(id)
        if not product:
            response_object = {
                'status': 'fail',
                'message': 'Product not found.'
            }
            return response_object, 404
        else:
            return product


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
