from flask import Blueprint, jsonify, request
from flask_restplus import Api, Resource
from config import Config
from app.vendor.dao import UserDao
from app.vendor.models import User
from app.vendor.exception import ApplicationException
from app.vendor.api.user import api as user_ns
from app.vendor.api.appinfo import api as app_info_ns
from app.vendor.api.auth import api as auth_ns

apiv1 = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(apiv1, version=Config.CURRENT_VERSION, title='{} API'.format(Config.SERVICE_NAME),
          description='Application End Points',
          default=Config.SERVICE_NAME,
          default_label="{} v{}".format(Config.SERVICE_NAME, Config.CURRENT_VERSION))


api.add_namespace(user_ns, path="/user")
api.add_namespace(app_info_ns)
api.add_namespace(auth_ns)
