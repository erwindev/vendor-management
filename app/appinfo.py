from flask import Blueprint, jsonify, request
from flask_restx import Api, Namespace, Resource, fields
from app.config import Config
#from app.order.api.order import api as order_ns

# Create Blueprint first
appinfo_bp = Blueprint('appinfo', __name__)

# Then create Api instance with the Blueprint
api = Api(appinfo_bp, 
    title='App Info API',
    version='1.0',
    description='App information endpoints'
)

@api.route("/health")
class Health(Resource):
    def get(self):
        ''' Provides status of system '''
        return jsonify(status='UP')


@api.route("/info")
class Info(Resource):
    def get(self):
        ''' Provides name and current version '''
        return jsonify(name=Config.SERVICE_NAME, version=Config.CURRENT_VERSION)
