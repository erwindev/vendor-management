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
        'create_date': fields.Date(),
        'last_login_date': fields.Date(),
        'updated_date' :fields.Date(),
        'status': fields.String()
    })         
    changepassword = api.model('changepassword', {
        'id': fields.String(required=True),
        'password': fields.String(required=True),
        'newpassword': fields.String(required=True)        
    })         
    message = api.model('message', {
        'status': fields.String(required=True),
        'message': fields.String(required=True),
    })    
    result =  api.model('result', {
        'user': fields.Nested(user),
        'result': fields.Nested(message)
    })    
    resultlist =  api.model('resultlist', {
        'userlist': fields.List(fields.Nested(user)),
        'result': fields.Nested(message)
    })     

api = UserDto.api


@api.route('')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class UserList(Resource):

    @api.doc('list_of_registered_users')
    @api.marshal_with(UserDto.resultlist, code=200, description='Successful')
    @token_required
    def get(self):
        """Get all users"""
        try:
            users = UserDao.get_all()
            user_ret_list = []
            for user in users:
                user.password = None
                user_ret_list.append(user.to_json())

            result = {
                'status': 'success',
                'message': 'User list returned.'
            }             
            response_object = {
                'userlist': user_ret_list,
                'result': result
            }                
            return response_object, 200
        except Exception as e:
            result = {
                'status': 'error',
                'message': 'Internal Server Error'
            }             
            response_object = {
                'userlist': None,
                'result': result
            }
            return response_object, 500    

    @api.marshal_with(UserDto.message, code=201, description='User successfully created.')
    @api.response(code=409, description='User cannot be created.') 
    @api.doc('create a new user')
    @api.expect(UserDto.user, validate=True)
    def post(self):
        """Insert a user"""
        try:
            user_data = request.json

            if UserDao.get_by_email(user_data['email']) is not None:
                response_object = {
                    'status': 'fail',
                    'message': 'User cannot be created.'
                }
                return response_object, 409

            if UserDao.get_by_email(user_data['email']) is not None:
                response_object = {
                    'status': 'fail',
                    'message': 'User cannot be created.'
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
                'message': 'User successfully created.'
            }
            return response_object, 201
        except Exception as e:
            response_object = {
                'status': 'error',
                'message': 'Internal Server Error'
            }
            return response_object, 500            


    @api.doc('update a user')
    @api.expect(UserDto.user, validate=False)
    @api.marshal_with(UserDto.result, code=201, description='User successfully updated.')
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
            result = {
                'status': 'success',
                'message': 'User successfully updated.'
            } 
            response_object = {
                'user': existing_user,
                'result': result,
            }                     
            return response_object, 201
        except Exception as e:
            result = {
                'status': 'error',
                'message': 'Internal Server Error'
            }
            response_object = {
                'user': None,
                'result': result,
            }                
            return response_object, 500             


@api.route('/<id>')
@api.param('id', 'The User identifier')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class User(Resource):

    @api.doc('get a user')
    @api.marshal_with(UserDto.result, code=200, description='User found.')
    @api.response(code=404, description='User not found.')
    @token_required
    def get(self, id):
        """Get a user given its identifier"""
        user = UserDao.get_by_id(id)
        if not user:
            result = {
                'status': 'fail',
                'message': 'User not found.'
            } 
            response_object = {
                'user': None,
                'result': result,
            }               
            return response_object, 404
        else:
            result = {
                'status': 'success',
                'message': 'User found.'
            } 
            response_object = {
                'user': user,
                'result': result,
            }                    
            return response_object, 200


@api.route("/changepassword")
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class UserChangePassword(Resource):

    @api.doc('change passwqord')
    @api.expect(UserDto.changepassword, validate=True)
    @api.marshal_with(UserDto.message, code=201, description='Password changed.')
    @api.response(code=401, description='Password cannot be changed.')
    def post(self):
        """Change password"""
        try:
            user_data = request.json

            user = UserDao.get_by_id(user_data['id'])

            if user is not None and user.check_password(user_data['password']):
                new_user = UserDao.change_password(user.id, user_data['newpassword'])
                response_object = {
                    'status': 'success',
                    'message': 'Password changed.'
                }
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Password cannot be changed.'
                }                
                return response_object, 401                

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
