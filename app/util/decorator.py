from functools import wraps
from flask import request
import jwt
from app.config import Config


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Remove 'Bearer ' prefix
            except IndexError:
                token = auth_header

        if not token:
            return {
                'message': 'Token is missing.',
                'error': 'Unauthorized'
            }, 401

        try:
            # Remove decode() as jwt.decode() already returns a dict in newer versions
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            
        except jwt.ExpiredSignatureError:
            return {
                'message': 'Token has expired.',
                'error': 'Unauthorized'
            }, 401
        except jwt.InvalidTokenError:
            return {
                'message': 'Invalid token.',
                'error': 'Unauthorized'
            }, 401
            
        return f(*args, **kwargs)

    return decorated            