from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from app.user.dao.user import UserDao, BlackListTokenDao
from app.user.models.user import User, BlackListToken
from app.util.exception import ApplicationException
from app.util import TokenUtil
import logging


# Data Transfer Object for authentication-related API models
class AuthDto:
    # Create namespace for authentication operations
    api = Namespace('auth', description='authentication related operations')
    
    # Model for login request data validation
    logindata = api.model('logindata', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
    
    # Model for authentication response data
    authdata = api.model('authdata', {
        'firstname': fields.String(required=True, description='First name'),
        'lastname': fields.String(required=True, description='Last name'),
        'email': fields.String(required=True, description='Email'),
        'create_date': fields.Date(description='Create Date'),
        'last_login_date': fields.Date(description='Last Login Date'),
        'updated_date': fields.Date(description='Updated Date'),
        'is_admin': fields.String(required=True, description='Admin'),
        'id': fields.String(required=True, description='User id'),
        'token': fields.String(required=True, description='Auth token'),
    })
    
    # Model for generic message responses
    message = api.model('message', {
        'status': fields.String(required=True),
        'message': fields.String(required=True),
    })
    
    # Combined model for full authentication response
    result =  api.model('result', {
        'authdata': fields.Nested(authdata),
        'result': fields.Nested(message)
    })

# Create API instance from AuthDto
api = AuthDto.api

@api.route('/login')
class UserLogin(Resource):
    """User Login Resource - Handles user authentication"""
    
    @api.doc('user login')
    @api.expect(AuthDto.logindata, validate=True)
    @api.marshal_with(AuthDto.result, code=200, description='Successful user login.')
    @api.response(code=401, description='Email or password does not match.')
    def post(self):
        try:
            # Extract login credentials from request
            post_data = request.json
            # Attempt to retrieve user by email
            user = UserDao.get_by_email(email=post_data.get('email'))
            
            # Validate user credentials
            if not user or not user.check_password(post_data.get('password')):
                return {
                    'authdata': None,
                    'result': {
                        'status': 'fail',
                        'message': 'Email or password does not match.'
                    }
                }, 401

            # Generate authentication token
            auth_token = TokenUtil.encode_token(user.id)
            if not auth_token:
                raise ApplicationException("Failed to generate auth token")

            # Update user's last login timestamp
            UserDao.set_last_login_date(user.id)
            
            # Return successful login response with user data and token
            return {
                'authdata': {
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'email': user.email,
                    'is_admin': 0,
                    'id': user.id,
                    'create_date': user.create_date,
                    'updated_date': user.updated_date,
                    'last_login_date': user.last_login_date,
                    'token': auth_token
                },
                'result': {
                    'status': 'success',
                    'message': 'Successful user login.'
                }
            }, 200

        except Exception as e:
            # Log any unexpected errors and return generic error response
            logging.error(f"Login failed: {str(e)}")
            return {
                'authdata': None,
                'result': {
                    'status': 'fail',
                    'message': 'Internal Server Error'
                }
            }, 500


@api.route('/logout')
@api.header('Authorization: Bearer', 'JWT TOKEN', required=True)
class LogoutApi(Resource):     
    """Logout Resource - Handles user logout and token invalidation"""

    @api.marshal_with(AuthDto.message, code=200, description='Successfully logged out.')    
    @api.response(code=403, description='Provide a valid auth token.')
    @api.response(code=401, description='Token is blacklisted.')    
    def post(self):
        # Extract token from Authorization header
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split(" ")[1] if auth_header else ''
        
        # Validate token presence
        if not auth_token:
            return {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }, 403

        # Check if token is already blacklisted
        if BlackListToken.check(auth_token):
            return {
                'status': 'fail',
                'message': 'Token is blacklisted.'
            }, 403
        
        # Validate token authenticity
        resp = TokenUtil.decode_token(auth_token)
        if isinstance(resp, str):
            return {
                'status': 'fail',
                'message': resp
            }, 401

        # Blacklist the token and return success response
        BlackListTokenDao.save_token(auth_token)
        return {
            'status': 'success',
            'message': 'Successfully logged out.'
        }, 200
                
