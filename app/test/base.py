import unittest
import json
from flask_testing import TestCase

from app import db
from application import app
from app.vendor.models.user import User


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):        
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        user = User()
        user.firstname = 'joe'
        user.lastname = 'tester'
        user.email = 'joetester@se.com'
        user.set_password('test')
        user.username = 'joe.tester'
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @staticmethod
    def login_user():
        return app.test_client().post(
            '/api/v1/auth/login',
            data=json.dumps(dict(
                username='joe.tester',
                password='test'
            )),
            content_type='application/json'
        )

    @staticmethod
    def get_token_and_loggedin_user():
        response = BaseTestCase.login_user()
        data = json.loads(response.data.decode())
        user_loggedin_data = json.loads(response.data.decode())                  
        auth_token = user_loggedin_data['Authorization']      
        return auth_token, user_loggedin_data  

    @staticmethod
    def logged_out(auth_token):
        return app.test_client().post(
            '/api/v1/auth/logout',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )           
