from flask import Blueprint, jsonify, request
from flask_restx import Api
from app.config import Config
from app.vendor.api.vendor import api as vendor_ns

vendor_apiv1 = Blueprint('vendor_api', __name__, url_prefix='/v/v1')

vendor_api = Api(vendor_apiv1, version=Config.CURRENT_VERSION, title='{} Vendor API'.format(Config.SERVICE_NAME),
          description='Vendor End Points',
          default=Config.SERVICE_NAME,
          default_label="{} v{}".format(Config.SERVICE_NAME, Config.CURRENT_VERSION))

vendor_api.add_namespace(vendor_ns, path="/vendor")

from app.appinfo import api as appinfo_ns
vendor_api.add_namespace(appinfo_ns, path="/app")

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    },
}

vendor_api.authorizations = authorizations
vendor_api.security = 'Bearer Auth'
