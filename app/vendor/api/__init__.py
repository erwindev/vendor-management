from flask import Blueprint, jsonify, request
from flask_restplus import Api
from app.config import Config
from app.vendor.api.user import api as user_ns
from app.vendor.api.appinfo import api as app_info_ns
from app.vendor.api.auth import api as auth_ns
from app.vendor.api.vendor import api as vendor_ns
from app.vendor.api.contact import api as contact_ns
from app.vendor.api.product import api as product_ns

apiv1 = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(apiv1, version=Config.CURRENT_VERSION, title='{} API'.format(Config.SERVICE_NAME),
          description='Application End Points',
          default=Config.SERVICE_NAME,
          default_label="{} v{}".format(Config.SERVICE_NAME, Config.CURRENT_VERSION))


api.add_namespace(auth_ns)
api.add_namespace(user_ns, path="/user")
api.add_namespace(vendor_ns, path="/vendor")
api.add_namespace(product_ns, path="/product")
api.add_namespace(contact_ns, path="/contact")
api.add_namespace(app_info_ns)
