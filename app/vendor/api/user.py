import sys
from flask import jsonify, request
from flask_restplus import Api, Resource, Namespace, fields
from app.vendor.dao.user import UserDao
from app.vendor.models.user import User as UserModel
from app.vendor.exception import ApplicationException
from app.vendor.util.decorator import token_required


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'id': fields.String(),
        'firstname': fields.String(required=True),
        'lastname': fields.String(required=True),
        'email': fields.String(required=True),
        'password': fields.String(required=True),
        'create_date': fields.DateTime(),
        'last_login_date': fields.String(),
        'status': fields.String()
    })         

api = UserDto.api


@api.route("/")
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class UserList(Resource):

    @api.doc('list_of_registered_users')
    @api.marshal_list_with(UserDto.user, envelope='userlist')
    @token_required
    def get(self):
        """Get all users"""
        try:
            users = UserDao.get_all()
            user_ret_list = []
            for user in users:
                user.password = None
                user_ret_list.append(user.to_json())
            return user_ret_list
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500    

    @api.response(201, 'User successfully created.')
    @api.response(409, 'User already exists.')
    @api.doc('create a new user')
    @api.expect(UserDto.user, validate=True)
    def post(self):
        """Insert a user"""
        try:
            user_data = request.json

            if UserDao.get_by_email(user_data['email']) is not None:
                response_object = {
                    'status': 'fail',
                    'message': 'User already exists.'
                }
                return response_object, 409

            if UserDao.get_by_email(user_data['email']) is not None:
                response_object = {
                    'status': 'fail',
                    'message': 'User already exists.'
                }
                return response_object, 409

            new_user = UserModel()
            new_user.firstname = user_data['firstname']
            new_user.lastname = user_data['lastname']
            new_user.email = user_data['email']
            new_user.set_password(user_data['password'])
            new_user = UserDao.save_user(new_user)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500


    @api.response(201, 'User successfully updated.')
    @api.doc('update a user')
    @api.expect(UserDto.user, validate=False)
    @token_required
    def put(self):
        """Update a user"""
        try:
            user_data = request.json
            existing_user = UserDao.get_by_id(user_data['id'])

            if 'firstname' in user_data:
                existing_user.firstname = user_data['firstname']

            if 'lastname' in user_data:
                existing_user.lastname = user_data['lastname']

            if 'password' in user_data:
                existing_user.set_password(user_data['password'])                

            if 'status' in user_data:
                existing_user.status = user_data['status']
                
            existing_user = UserDao.update_user(existing_user)
            response_object = {
                'status': 'success',
                'message': 'Successfully updated.'
            }
            return response_object, 201
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Internal Server Error'
            }, 500            


@api.route('/<id>')
@api.param('id', 'The User identifier')
@api.response(404, 'User not found.')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class User(Resource):

    @api.doc('get a user')
    @api.marshal_with(UserDto.user)
    @token_required
    def get(self, id):
        """Get a user given its identifier"""
        user = UserDao.get_by_id(id)
        if not user:
            response_object = {
                'status': 'fail',
                'message': 'User not found.'
            }
            return response_object, 404
        else:
            return user


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
