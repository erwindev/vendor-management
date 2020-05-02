from flask import Blueprint, jsonify, request
from flask_restplus import Api
from app.config import Config
from app.user.api.user import api as user_ns
from app.user.api.auth import api as auth_ns

user_apiv1 = Blueprint('user_api', __name__, url_prefix='/u/api/v1')

user_api = Api(user_apiv1, version=Config.CURRENT_VERSION, title='{} User API'.format(Config.SERVICE_NAME),
          description='User End Points',
          default=Config.SERVICE_NAME,
          default_label="{} v{}".format(Config.SERVICE_NAME, Config.CURRENT_VERSION))

user_api.add_namespace(auth_ns, path="/auth")
user_api.add_namespace(user_ns, path="/user")

from app.appinfo import api as appinfo_ns
user_api.add_namespace(appinfo_ns, path="/app")
