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
        'vendor_id': fields.String(required=True),
        'product_name': fields.String(required=True),
        'status': fields.String(),
        'create_date': fields.Date(),
        'updated_date': fields.Date(),
        'user_by': fields.String(required=True)        
    })      


api = ProductDto.api

@api.route("/vendor/<vendor_id>")
@api.param('vendor_id', 'The Vendor identifier')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class ProductList(Resource):

    @api.doc('list_of_product_by_vendor')
    @api.marshal_list_with(ProductDto.product, envelope='productlist')
    @token_required
    def get(self, vendor_id):
        """ Get all products by vendor"""
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


@api.route('')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class Product(Resource):
    @api.response(201, 'Product successfully created.')
    @api.doc('create a new product')
    @api.expect(ProductDto.product, validate=True)
    @token_required
    def post(self):
        """Insert a product"""
        try:
            product_data = request.json

            new_product = ProductModel()
            new_product.vendor_id = product_data['vendor_id']
            new_product.product_name = product_data['product_name']
            new_product.status = product_data['status']
            new_product.user_by = product_data['user_by']
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
    def put(self):
        """Update a product"""
        try:
            product_data = request.json

            existing_product = ProductModel()
            existing_product.id = product_data['id']
            if 'vendor_id' in product_data:
                existing_product.vendor_id = product_data['vendor_id']

            if 'product_name' in product_data:
                existing_product.product_name = product_data['product_name']
            
            if 'status' in product_data:
                existing_product.status = product_data['status']     

            if 'user_by' in product_data:
                existing_product.user_by = product_data['user_by']                             

            existing_product = ProductDao.update_product(existing_product)
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



@api.route('/<product_id>')
@api.param('product_id', 'The Product identifier')
@api.response(404, 'Product not found.')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class ProductDetail(Resource):

    @api.doc('get a product')
    @api.marshal_with(ProductDto.product)
    @token_required
    def get(self, product_id):
        """Get a product given its identifier"""
        product = ProductDao.get_by_id(product_id)
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
