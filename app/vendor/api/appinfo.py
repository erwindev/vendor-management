from flask import jsonify
from flask_restplus import Api, Resource, Namespace
from app.config import Config

class AppInfoDto:
    api = Namespace('appinfo', description='appinfo related operations')

api = AppInfoDto.api

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
