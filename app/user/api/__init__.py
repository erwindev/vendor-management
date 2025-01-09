from flask import Blueprint
from flask_restx import Api
from app.config import Config
from app.user.api.user import api as user_ns
from app.user.api.auth import api as auth_ns

user_apiv1 = Blueprint('user_api', __name__, url_prefix='/u/v1')

user_api = Api(user_apiv1, version=Config.CURRENT_VERSION, title='{} User and Auth API'.format(Config.SERVICE_NAME),
          description='User End Points',
          default=Config.SERVICE_NAME,
          default_label="{} v{}".format(Config.SERVICE_NAME, Config.CURRENT_VERSION))

user_api.add_namespace(auth_ns, path="/auth")
user_api.add_namespace(user_ns, path="/user")

from app.appinfo import api as appinfo_ns
user_api.add_namespace(appinfo_ns, path="/app")

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    },
}

user_api.authorizations = authorizations
user_api.security = 'Bearer Auth'
