import unittest
import json

from app import db
from app.test.base import BaseTestCase


class TestUserResgistration(BaseTestCase):
    def test_registration(self):
        """ Test for user registration """
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user()
        with self.client:
            response = BaseTestCase().register_user(auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered username"""
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user()

        # register user
        BaseTestCase.register_user(auth_token)
        with self.client:
            # register user again
            response = BaseTestCase().register_user(auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User already exists.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 409)


class TestUser(BaseTestCase):
    def test_get_user(self):
        """ Test for getting user """
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user()
        with self.client:
            user_id = user_loggedin_data['user_id']
            response = BaseTestCase().get_user(auth_token, user_id)
            data = json.loads(response.data.decode())
            self.assertTrue(data['username'] == 'joe.tester')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_get_all_user(self):
        """ Test for getting all users """
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user()
        with self.client:
            response = BaseTestCase().get_all_user(auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(len(data) == 1)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)      

    def test_update_user(self):
        """ Test for getting user """
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user()
        with self.client:
            user_id = user_loggedin_data['user_id']
            # get logged in user
            response = BaseTestCase().get_user(auth_token, user_id)
            data = json.loads(response.data.decode())
            self.assertTrue(data['username'] == 'joe.tester')
            self.assertTrue(data['firstname'] == 'joe')
            self.assertTrue(data['lastname'] == 'tester')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)          

            # update logged in user
            response = BaseTestCase().update_user(auth_token, user_id, 'joex', 'testerx', 'act')    
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)    

            #get user
            response = BaseTestCase().get_user(auth_token, user_id)
            data = json.loads(response.data.decode())
            self.assertTrue(data['username'] == 'joe.tester')
            self.assertTrue(data['firstname'] == 'joex')
            self.assertTrue(data['lastname'] == 'testerx')
            self.assertTrue(data['status'] == 'act')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)                           


class TestLogout(BaseTestCase):

    def test_successful_logout(self):
        """ Test for logging out user """
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user()
        with self.client:
            # logout user using a valid token
            response = BaseTestCase.logged_out(auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)            

            # logout user using a blacklisted token
            response = BaseTestCase.logged_out(auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Token is blacklisted.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 403)             

            # logout user using an invalid token
            response = BaseTestCase.logged_out('xxx')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid token.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)                          


if __name__ == '__main__':
    unittest.main()