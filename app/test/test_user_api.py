import unittest
import json

from app import db
from app.test.base import BaseTestCase


def login_user(self):
    return self.client.post(
        '/api/v1/auth/login',
        data=json.dumps(dict(
            username='joe.tester',
            password='test'
        )),
        content_type='application/json'
    )


def register_user(self, auth_token):
    return self.client.post(
        '/api/v1/user/',
        headers=dict(
            Authorization='Bearer {}'.format(auth_token) 
        ),        
        data=json.dumps(dict(
            email='ealberto-test@me.com',
            username='ealberto-test',
            firstname='erwin',
            lastname='alberto',
            password='test'
        )),
        content_type='application/json'
    )


def get_user(self, auth_token, user_id):
    return self.client.get(
        '/api/v1/user/{}'.format(user_id),
        headers=dict(
            Authorization='Bearer {}'.format(auth_token) 
        ),        
        content_type='application/json'
    )    


def logged_out(self, auth_token):
    return self.client.post(
        '/api/v1/auth/logout',
        headers=dict(
            Authorization='Bearer {}'.format(auth_token) 
        ),        
        content_type='application/json'
    )    



class TestUserResgistration(BaseTestCase):
    def test_registration(self):
        """ Test for user registration """
        with self.client:

            response = login_user(self)
            user_loggedin_data = json.loads(response.data.decode())                  
            auth_token = user_loggedin_data['Authorization']

            response = register_user(self, auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered username"""
        response = login_user(self)
        user_loggedin_data = json.loads(response.data.decode())                  
        auth_token = user_loggedin_data['Authorization']

        register_user(self, auth_token)
        with self.client:
            response = register_user(self, auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User already exists.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 409)


class TestUser(BaseTestCase):
    def test_get_user(self):
        """ Test for getting user """
        with self.client:

            response = login_user(self)
            user_loggedin_data = json.loads(response.data.decode())                  
            auth_token = user_loggedin_data['Authorization']
            user_id = user_loggedin_data['user_id']

            response = get_user(self, auth_token, user_id)
            data = json.loads(response.data.decode())
            self.assertTrue(data['username'] == 'joe.tester')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)


class TestLogout(BaseTestCase):
    def test_successful_logout(self):
        """ Test for logging out user """
        with self.client:

            response = login_user(self)
            user_loggedin_data = json.loads(response.data.decode())                  
            auth_token = user_loggedin_data['Authorization']

            response = logged_out(self, auth_token, user_id)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'USuccessfully logged out.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)     


    def test_successful_logout(self):
        """ Test for logging out user """
        with self.client:

            response = login_user(self)
            user_loggedin_data = json.loads(response.data.decode())                  
            auth_token = user_loggedin_data['Authorization']

            response = logged_out(self, auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)            

            response = logged_out(self, auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Token blacklisted.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)             

            response = logged_out(self, 'xxx')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid token.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)                          


if __name__ == '__main__':
    unittest.main()