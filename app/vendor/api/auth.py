from flask import jsonify, request
from flask_restplus import Api, Resource, Namespace, fields
from app.vendor.dao.user import UserDao, BlackListTokenDao
from app.vendor.models.user import User, BlackListToken
from app.vendor.exception import ApplicationException
from app.vendor.util.token_util import TokenUtil


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'username': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

api = AuthDto.api
_user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(_user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        try:
            user = UserDao.get_by_username(post_data['username'])
            if user and user.check_password(post_data['password']):
                auth_token = TokenUtil.encode_token(user.id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'user_id': user.id,
                        'Authorization': auth_token.decode()
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'username or password does not match.'
                }
                return response_object, 401   
        except ApplicationException as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500       


@api.route('/logout')
@api.header('Authorization: Bearer', 'JWT TOKEN', required=True)
class LogoutApi(Resource):     

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
                
