from flask import Blueprint, jsonify, request
from flask_restx import Api
from app.config import Config
from app.contact.api.contact import api as contact_ns

contact_apiv1 = Blueprint('contact_api', __name__, url_prefix='/c/v1')

contact_api = Api(contact_apiv1, version=Config.CURRENT_VERSION, title='{} Contact API'.format(Config.SERVICE_NAME),
          description='Contact End Points',
          default=Config.SERVICE_NAME,
          default_label="{} v{}".format(Config.SERVICE_NAME, Config.CURRENT_VERSION))

contact_api.add_namespace(contact_ns, path="/contact")

from app.appinfo import api as appinfo_ns
contact_api.add_namespace(appinfo_ns, path="/app")

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    },
}

contact_api.authorizations = authorizations
contact_api.security = 'Bearer Auth'