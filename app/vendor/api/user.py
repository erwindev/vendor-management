import sys
from flask import jsonify, request
from flask_restplus import Api, Resource, Namespace, fields
from app.vendor.dao.user import UserDao
from app.vendor.models.user import User as UserModel
from app.vendor.exception import ApplicationException
from app.vendor.util.decorator import token_required


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'id': fields.String(),
        'firstname': fields.String(required=True),
        'lastname': fields.String(required=True),
        'username': fields.String(required=True),
        'email': fields.String(required=True),
        'created_date': fields.DateTime(required=True),
        'last_login_date': fields.String(required=True)
    })
    ruser = api.model('user', {
            'firstname': fields.String(required=True),
            'lastname': fields.String(required=True),
            'username': fields.String(required=True),
            'email': fields.String(required=True),
            'password': fields.String(required=True)
        })     


api = UserDto.api

@api.route("/")
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class UserList(Resource):
    """
    This class contains the functions to run the API request.
    HTTP methods are implemented as functions.  Currently,
    this API only supports HTTP GET
    """

    @api.doc('list_of_registered_users')
    @api.marshal_list_with(UserDto.user, envelope='userlist')
    @token_required
    def get(self):
        """Get all users"""
        try:
            users = UserDao.get_all()
            user_ret_list = []
            for user in users:
                user_ret_list.append(user.to_json())
            return user_ret_list
        except ApplicationException as e:
            error_message = str(e)
            return jsonify(error_message=error_message[:200])

    @api.response(201, 'User successfully created.')
    @api.response(409, 'User already exists.')
    @api.doc('create a new user')
    @api.expect(UserDto.ruser, validate=False)
    @token_required
    def post(self):
        """Insert a user"""
        try:
            user_data = request.json

            # ToDo: need to add logic to check if email and user already exist
            if UserDao.get_by_email(user_data['email']) is not None:
                return "User already exist", 409

            if UserDao.get_by_username(user_data['username']) is not None:
                return "User already exist", 409

            new_user = UserModel()
            new_user.firstname = user_data['firstname']
            new_user.lastname = user_data['lastname']
            new_user.username = user_data['username']
            new_user.email = user_data['email']
            new_user.set_password(user_data['password'])
            new_user = UserDao.save_user(new_user)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        except Exception as e:
            api.abort(500)


@api.route('/<id>')
@api.param('id', 'The User identifier')
@api.response(404, 'User not found.')
@api.expect(api.parser().add_argument('Authorization', location='headers'))
class User(Resource):

    @api.doc('get a user')
    @api.marshal_with(UserDto.user)
    @token_required
    def get(self, id):
        """Get a user given its identifier"""
        user = UserDao.get_by_id(id)
        if not user:
            api.abort(404)
        else:
            return user


@api.errorhandler(Exception)
def generic_exception_handler(e: Exception):
    exc_type, exc_value, exc_traceback = sys.exc_info()

    if exc_traceback:
        traceback_details = {
            'filename': exc_traceback.tb_frame.f_code.co_filename,
            'lineno': exc_traceback.tb_lineno,
            'name': exc_traceback.tb_frame.f_code.co_name,
            'message': str(exc_value),
        }
        return {
            'status': 'error',
            'message': traceback_details['message']
        }, 500
    else:
        return {
            'status': 'error',
            'message': 'Internal Server Error'
        }, 500    
