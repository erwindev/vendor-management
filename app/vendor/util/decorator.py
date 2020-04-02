from functools import wraps
from flask import request
from app.vendor.api.auth import Util


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Util.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated