import unittest
import json
from app.user.test.base import UserBaseTestCase
from app.util.test.base import BaseTestCase
import logging
from app.util.constants import TEST_USER_EMAIL, TEST_USER_PASSWORD

class TestUserResgistration(UserBaseTestCase):

    def test_registration(self):
        """ Test for user registration """
        auth_token, user_loggedin_data = self.get_token_and_loggedin_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        with self.client:
            try:
                response = self.register_user(auth_token)
                
                if response.status_code == 404:
                    self.fail("Endpoint not found. Check URL path.")
                
                if not response.data:
                    self.fail("Empty response received")
                    
                data = json.loads(response.data.decode())
                self.assertTrue(data['status'] == 'success')
            except Exception as e:
                logging.error(f"Error occurred: {str(e)}")
                raise

    def test_registered_with_already_registered_user(self):
        """
        Test registration with duplicate user credentials
        Expected behavior: Should return 409 Conflict status code
        """
        auth_token, user_loggedin_data = self.get_token_and_loggedin_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        with self.client:
            try:
                # First registration attempt should succeed
                response = self.register_user(auth_token)
                
                # Second registration attempt with same credentials should fail
                response = self.register_user(auth_token)
                
                data = json.loads(response.data.decode())
                
                self.assertEqual(response.status_code, 409)  # Conflict status code
                self.assertEqual(data.get('status'), 'fail')
            except Exception as e:
                logging.error(f"Error occurred: {str(e)}")
                raise

    def test_get_user(self):
        """Test for getting user"""
        auth_token, user_loggedin_data = self.get_token_and_loggedin_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        with self.client:
            try:
                # First register a user
                reg_response = self.register_user(auth_token)
                reg_data = json.loads(reg_response.data.decode())
                
                # Get user ID from response
                user_id = reg_data.get('id')
                if not user_id:
                    self.fail("No user ID in registration response")
                
                # Then try to get the user
                response = self.get_user(auth_token, user_id)
                self.assertEqual(response.status_code, 200)
                
                data = json.loads(response.data.decode())


                # Verify user data directly without checking status
                self.assertEqual(data['user']['email'], 'ealberto-test@me.com')
                self.assertEqual(data['user']['firstname'], 'erwin')
                self.assertEqual(data['user']['lastname'], 'alberto')
                
            except Exception as e:
                logging.error(f"Error occurred: {str(e)}")
                raise

    def test_get_all_user(self):
        """ Test for getting all users """
        auth_token, user_loggedin_data = self.get_token_and_loggedin_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        with self.client:
            response = self.get_all_user(auth_token)
            data = json.loads(response.data.decode())
            
            # Check response structure
            self.assertIn('userlist', data)
            self.assertIn('result', data)
            
            # Check userlist
            userlist = data['userlist']
            self.assertIsInstance(userlist, list)
            self.assertTrue(len(userlist) >= 1)
            
            # Check first user
            first_user = userlist[0]
            self.assertIn('email', first_user)
            self.assertIn('firstname', first_user)
            self.assertIn('lastname', first_user)
            
            # Check result
            result = data['result']
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['message'], 'User list returned.')
            
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        """
        Test user profile update functionality
        Steps:
        1. Get current user details
        2. Update user information
        3. Verify the updates were successful
        """
        auth_token, user_loggedin_data = self.get_token_and_loggedin_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        user_id = user_loggedin_data['authdata']['id']
        with self.client:
            # Fetch initial user details
            response = self.get_user(auth_token, user_id)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            # Verify initial state before updates
            self.assertEqual(data['user']['email'], TEST_USER_EMAIL)
            self.assertEqual(data['user']['firstname'], 'joe')
            self.assertEqual(data['user']['lastname'], 'tester')

            # Perform user update
            response = self.update_user(
                auth_token, 
                user_id,
                'joex',
                'testerx',
                'act'
            )
            update_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            # Verify the updates were applied correctly
            response = self.get_user(auth_token, user_id)
            data = json.loads(response.data.decode())
            self.assertEqual(data['user']['email'], 'joetester@se.com')
            self.assertEqual(data['user']['firstname'], 'joex')
            self.assertEqual(data['user']['lastname'], 'testerx')
            self.assertEqual(data['user']['status'], 'act')
            self.assertEqual(response.status_code, 200)

    def test_changepassword(self):                         
        """ Test for changing password """
        try:
            auth_token, user_loggedin_data = self.get_token_and_loggedin_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
            user_id = user_loggedin_data['authdata']['id']
            # Get user details using self.auth_token and self.user_id from setUp
            response = self.get_user(auth_token, user_id)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')
            
            # Verify initial user data
            self.assertEqual(data['user']['email'], TEST_USER_EMAIL)
            self.assertEqual(data['user']['firstname'], 'joe')
            self.assertEqual(data['user']['lastname'], 'tester')

            # Change password
            response = self.change_password(
                auth_token, 
                user_id, 
                TEST_USER_PASSWORD,
                'my-new-password'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            # Try login with new password
            response = self.login_user(TEST_USER_EMAIL, 'my-new-password')

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('authdata', data)
            self.assertIn('token', data['authdata'])
            self.assertEqual(data['authdata']['email'], TEST_USER_EMAIL)
            
        except Exception as e:
            logging.error(f"Test failed with error: {str(e)}")
            raise


    def test_successful_logout(self):
        """ Test for logout functionality with different token scenarios """
        auth_token, user_loggedin_data = self.get_token_and_loggedin_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        with self.client:
            try:
                # Test Case 1: Valid token logout
                response = self.logged_out(auth_token)
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.content_type, 'application/json')
                self.assertEqual(data['status'], 'success')
                self.assertEqual(data['message'], 'Successfully logged out.')

                # Test Case 2: Blacklisted token logout
                response = self.logged_out(auth_token)
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 403)
                self.assertEqual(response.content_type, 'application/json')
                self.assertEqual(data['status'], 'fail')
                self.assertEqual(data['message'], 'Token is blacklisted.')

                # Test Case 3: Invalid token logout
                response = self.logged_out('xxx')
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 401)
                self.assertEqual(response.content_type, 'application/json')
                self.assertEqual(data['status'], 'fail')
                self.assertEqual(data['message'], 'Invalid token.')

            except Exception as e:
                logging.error(f"Test failed with error: {str(e)}")
                raise


if __name__ == '__main__':
    unittest.main()
