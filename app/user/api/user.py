import sys
from flask import jsonify, request
from flask_restx import Api, Resource, Namespace, fields
from app.user.dao.user import UserDao
from app.user.models.user import User as UserModel
from app.util.exception import ApplicationException
from app.util.decorator import token_required
from typing import Dict, Any
from http import HTTPStatus


def create_response(status: str, message: str, data: Dict = None, status_code: int = HTTPStatus.OK) -> tuple:
    """
    Helper function to create standardized API responses
    
    Args:
        status (str): Status of the response ('success' or 'fail')
        message (str): Message to be included in response
        data (Dict, optional): Additional data to include in response
        status_code (int, optional): HTTP status code, defaults to 200 OK
    
    Returns:
        tuple: Response dictionary and status code
    """
    response = {
        'status': status,
        'message': message
    }
    if data:
        response.update(data)
    return response, status_code


class UserDto:
    """Data Transfer Object for User API models"""
    api = Namespace('user', description='user related operations')
    
    # Model for user data validation and serialization
    user = api.model('user', {
        'id': fields.String(),
        'firstname': fields.String(required=True),
        'lastname': fields.String(required=True),
        'email': fields.String(required=True),
        'password': fields.String(required=True),
        'create_date': fields.Date(),
        'last_login_date': fields.Date(),
        'updated_date': fields.Date(),
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
        'id': fields.String(required=True)
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
    @api.marshal_with(UserDto.resultlist)
    @token_required
    def get(self):
        """
        Retrieve all users from the database
        
        Returns:
            dict: Contains list of users and result metadata
            int: HTTP status code
        
        Raises:
            ApplicationException: If there's an error retrieving users
        """
        try:
            # Fetch all users from database
            users = UserDao.get_all()
            # Convert user objects to JSON format
            user_ret_list = [user.to_json() for user in users]
            
            # Structure the response according to API specification
            response_data = {
                'userlist': user_ret_list,
                'result': {
                    'status': 'success',
                    'message': 'User list returned.'
                }
            }
            return response_data, HTTPStatus.OK
            
        except Exception as e:
            raise ApplicationException(str(e))

    @api.marshal_with(UserDto.message)
    @api.response(code=409, description='User cannot be created.') 
    @api.doc('create a new user')
    @api.expect(UserDto.user, validate=True)
    def post(self):
        """
        Create a new user
        
        Expected payload:
        {
            "firstname": "string",
            "lastname": "string",
            "email": "string",
            "password": "string"
        }
        
        Returns:
            tuple: Response containing status and user ID if successful
        
        Raises:
            ApplicationException: If user creation fails
        """
        try:
            user_data = request.json
            
            # Check if user with email already exists
            if UserDao.get_by_email(user_data['email']):
                return create_response(
                    'fail',
                    'User already exists.',
                    status_code=HTTPStatus.CONFLICT
                )

            # Create new user instance
            new_user = UserModel(
                firstname=user_data['firstname'],
                lastname=user_data['lastname'],
                email=user_data['email']
            )
            new_user.set_password(user_data['password'])
            new_user = UserDao.save_user(new_user)
            
            return create_response(
                'success',
                'User successfully created.',
                {'id': new_user.id},
                HTTPStatus.CREATED
            )
        except Exception as e:
            raise ApplicationException(str(e))


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
            return response_object, 200
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
    @api.doc('change password')
    @api.expect(UserDto.changepassword, validate=True)
    @api.marshal_with(UserDto.message)
    @api.response(code=401, description='Password cannot be changed.')
    def post(self):
        """
        Change user password
        
        Expected payload:
        {
            "id": "string",
            "password": "string",
            "newpassword": "string"
        }
        
        Returns:
            tuple: Response containing status and message
        
        Raises:
            ApplicationException: If password change fails
        """
        try:
            user_data = request.json
            
            # Verify user exists and current password is correct
            user = UserDao.get_by_id(user_data['id'])
            if not user or not user.check_password(user_data['password']):
                return create_response(
                    'fail',
                    'Password cannot be changed.',
                    status_code=HTTPStatus.UNAUTHORIZED
                )

            # Update password
            UserDao.change_password(user.id, user_data['newpassword'])
            return create_response('success', 'Password changed.')
            
        except Exception as e:
            raise ApplicationException(str(e))


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
