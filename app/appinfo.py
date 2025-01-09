from flask import Blueprint, jsonify
from flask_restx import Api, Resource
from app.config import Config

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
