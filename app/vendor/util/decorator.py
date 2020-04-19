from functools import wraps
from flask import request
from .token_util import TokenUtil
from app.vendor.dao.user import UserDao


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated


def get_logged_in_user(new_request):
    # get the auth token
    auth_token = new_request.headers.get('Authorization')
    
    if auth_token:                        
        auth_token = auth_token.split(' ')
        if len(auth_token) < 2:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401                        
        resp = TokenUtil.decode_token(auth_token[1])
        if not isinstance(resp, str):
            user = UserDao.get_by_id(resp)
            response_object = {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'email': user.email
                }
            }
            return response_object, 200
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
        return response_object, 401            