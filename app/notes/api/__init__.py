from flask import Blueprint, jsonify, request
from flask_restx import Api
from app.config import Config
from app.notes.api.notes import api as notes_ns

notes_apiv1 = Blueprint('notes_api', __name__, url_prefix='/n/v1')

notes_api = Api(notes_apiv1, version=Config.CURRENT_VERSION, title='{} Notes API'.format(Config.SERVICE_NAME),
          description='Notes End Points',
          default=Config.SERVICE_NAME,
          default_label="{} v{}".format(Config.SERVICE_NAME, Config.CURRENT_VERSION))

notes_api.add_namespace(notes_ns, path="/notes")

from app.appinfo import api as appinfo_ns
notes_api.add_namespace(appinfo_ns, path="/app")

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    },
}

notes_api.authorizations = authorizations
notes_api.security = 'Bearer Auth'