import json
from vms import app
from app.util.test.base import BaseTestCase

class UserBaseTestCase(BaseTestCase):

    ######################
    #
    # user api
    #
    ######################
    @staticmethod
    def register_user(auth_token):
        return app.test_client().post(
            '/u/api/v1/user',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                email='ealberto-test@me.com',
                firstname='erwin',
                lastname='alberto',
                password='test'
            )),
            content_type='application/json'
        )

    @staticmethod
    def update_user(auth_token, id, firstname, lastname, status):
        return app.test_client().put(
            '/u/api/v1/user',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                id=id,
                firstname=firstname,
                lastname=lastname,
                status=status
            )),
            content_type='application/json'
        )

    @staticmethod
    def change_password(auth_token, id, password, new_password):
        return app.test_client().post(
            '/u/api/v1/user/changepassword',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                id=id,
                password=password,
                newpassword=new_password
            )),
            content_type='application/json'
        )                

    @staticmethod
    def get_user(auth_token, id):
        return app.test_client().get(
            '/u/api/v1/user/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )    

    @staticmethod
    def get_all_user(auth_token):
        return app.test_client().get(
            '/u/api/v1/user',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )  
