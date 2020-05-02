from flask import jsonify, request
from flask_restplus import Api, Resource, Namespace, fields
from app.user.dao.user import UserDao, BlackListTokenDao
from app.user.models.user import User, BlackListToken
from app.util.exception import ApplicationException
from app.util import TokenUtil


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    logindata = api.model('logindata', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
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
    message = api.model('message', {
        'status': fields.String(required=True),
        'message': fields.String(required=True),
    })
    result =  api.model('result', {
        'authdata': fields.Nested(authdata),
        'result': fields.Nested(message)
    })

api = AuthDto.api


@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(AuthDto.logindata, validate=True)
    @api.marshal_with(AuthDto.result, code=200, description='Successful user login.')
    @api.response(code=401, description='Email or password does not match.')
    def post(self):
        # get the post data
        post_data = request.json
        try:
            user = UserDao.get_by_email(post_data['email'])
            if user and user.check_password(post_data['password']):
                auth_token = TokenUtil.encode_token(user.id)
                if auth_token:
                    authdata = {
                        'firstname': user.firstname,
                        'lastname': user.lastname,
                        'email': user.email,
                        'is_admin': 0,
                        'id': user.id,
                        'create_date': user.create_date,
                        'updated_date': user.updated_date,
                        'last_login_date': user.last_login_date,
                        'token': auth_token.decode()
                    }
                    result = {
                        'status': 'success',
                        'message': 'Successful user login.'
                    } 
                    response_object = {
                        'authdata': authdata,
                        'result': result,
                    }                  
                    UserDao.set_last_login_date(user.id)
                    return response_object, 200
            else:
                result = {
                    'status': 'fail',
                    'message': 'Email or password does not match.'
                }
                response_object = {
                    'authdata': None,
                    'result': result
                }
                return response_object, 401   
        except ApplicationException as e:
            result = {
                'status': 'fail',
                'message': 'Internal Server Error'
            }
            response_object = {
                'authdata': None,
                'result': result
            }
            return response_object, 500       


@api.route('/logout')
@api.header('Authorization: Bearer', 'JWT TOKEN', required=True)
class LogoutApi(Resource):     

    @api.marshal_with(AuthDto.message, code=200, description='Successfully logged out.')    
    @api.response(code=403, description='Provide a valid auth token.')
    @api.response(code=401, description='Token is blacklisted.')    
    def post(self):
        auth_header = request.headers.get('Authorization')

        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        
        if auth_token:
            is_blacklisted_token = BlackListToken.check(auth_token)
            if is_blacklisted_token:
                response_object = {
                    'status': 'fail',
                    'message': 'Token is blacklisted.'
                }                
                return response_object, 403
            
            resp = TokenUtil.decode_token(auth_token)

            if not isinstance(resp, str):
                BlackListTokenDao.save_token(auth_token)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403            
                
