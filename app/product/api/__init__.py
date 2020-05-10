from flask import Blueprint, jsonify, request
from flask_restplus import Api
from app.config import Config
from app.product.api.product import api as product_ns

product_apiv1 = Blueprint('product_api', __name__, url_prefix='/p/v1')

product_api = Api(product_apiv1, version=Config.CURRENT_VERSION, title='{} Product API'.format(Config.SERVICE_NAME),
          description='Product End Points',
          default=Config.SERVICE_NAME,
          default_label="{} v{}".format(Config.SERVICE_NAME, Config.CURRENT_VERSION))

product_api.add_namespace(product_ns, path="/product")

from app.appinfo import api as appinfo_ns
product_api.add_namespace(appinfo_ns, path="/app")
