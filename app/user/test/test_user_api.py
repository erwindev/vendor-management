import unittest
import json
from app.user.test.base import UserBaseTestCase
from app.util.test.base import BaseTestCase

class TestUserResgistration(UserBaseTestCase):
    def setUp(self):
        # Initialize base test cases and set up test environment
        BaseTestCase.setUp(self)
        UserBaseTestCase.setUp(self)
        
        # Authenticate test user and get access token
        self.auth_token, self.user_loggedin_data = self.get_token_and_loggedin_user('joetester@se.com', 'test')
        if not self.auth_token:
            raise Exception("Failed to get auth token")
        if not self.user_loggedin_data:
            raise Exception("Failed to get user data")
        
        # Extract user ID from login response, handling different possible response structures
        try:
            self.user_id = self.user_loggedin_data.get('user', {}).get('id')
            if not self.user_id:
                # Check alternative response formats for user ID
                self.user_id = (self.user_loggedin_data.get('authdata', {}).get('id') or 
                              self.user_loggedin_data.get('id'))
            
            if not self.user_id:
                raise KeyError("Could not find user ID in any expected location")
                
        except Exception as e:
            print("Login response structure:", self.user_loggedin_data)
            raise Exception(f"Could not find user ID in login response: {e}")

    def test_registration(self):
        """ Test for user registration """
        with self.client:
            try:
                response = self.register_user(self.auth_token)
                
                if response.status_code == 404:
                    self.fail("Endpoint not found. Check URL path.")
                
                if not response.data:
                    self.fail("Empty response received")
                    
                data = json.loads(response.data.decode())
                self.assertTrue(data['status'] == 'success')
            except Exception as e:
                print(f"Error occurred: {str(e)}")
                raise

    def test_registered_with_already_registered_user(self):
        """
        Test registration with duplicate user credentials
        Expected behavior: Should return 409 Conflict status code
        """
        with self.client:
            try:
                # First registration attempt should succeed
                response = self.register_user(self.auth_token)
                
                # Second registration attempt with same credentials should fail
                response = self.register_user(self.auth_token)
                
                data = json.loads(response.data.decode())
                
                self.assertEqual(response.status_code, 409)  # Conflict status code
                self.assertEqual(data.get('status'), 'fail')
            except Exception as e:
                print(f"Error occurred: {str(e)}")
                raise

    def test_get_user(self):
        """Test for getting user"""
        with self.client:
            try:
                # First register a user
                reg_response = self.register_user(self.auth_token)
                reg_data = json.loads(reg_response.data.decode())
                
                # Get user ID from response
                user_id = reg_data.get('id')
                if not user_id:
                    self.fail("No user ID in registration response")
                
                # Then try to get the user
                response = self.get_user(self.auth_token, user_id)
                self.assertEqual(response.status_code, 200)
                
                data = json.loads(response.data.decode())


                # Verify user data directly without checking status
                self.assertEqual(data['user']['email'], 'ealberto-test@me.com')
                self.assertEqual(data['user']['firstname'], 'erwin')
                self.assertEqual(data['user']['lastname'], 'alberto')
                
            except Exception as e:
                print(f"Error occurred: {str(e)}")
                raise

    def test_get_all_user(self):
        """ Test for getting all users """
        with self.client:
            response = self.get_all_user(self.auth_token)
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
        with self.client:
            # Fetch initial user details
            response = self.get_user(self.auth_token, self.user_id)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            # Verify initial state before updates
            self.assertEqual(data['user']['email'], 'joetester@se.com')
            self.assertEqual(data['user']['firstname'], 'joe')
            self.assertEqual(data['user']['lastname'], 'tester')

            # Perform user update
            response = self.update_user(
                self.auth_token, 
                self.user_id,
                'joex',
                'testerx',
                'act'
            )
            update_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            # Verify the updates were applied correctly
            response = self.get_user(self.auth_token, self.user_id)
            data = json.loads(response.data.decode())
            self.assertEqual(data['user']['email'], 'joetester@se.com')
            self.assertEqual(data['user']['firstname'], 'joex')
            self.assertEqual(data['user']['lastname'], 'testerx')
            self.assertEqual(data['user']['status'], 'act')
            self.assertEqual(response.status_code, 200)

    def test_changepassword(self):                         
        """ Test for changing password """
        try:
            # Get user details using self.auth_token and self.user_id from setUp
            response = self.get_user(self.auth_token, self.user_id)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')
            
            # Verify initial user data
            self.assertEqual(data['user']['email'], 'joetester@se.com')
            self.assertEqual(data['user']['firstname'], 'joe')
            self.assertEqual(data['user']['lastname'], 'tester')

            # Change password
            response = self.change_password(
                self.auth_token, 
                self.user_id, 
                'test', 
                'my-new-password'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            # Try login with new password
            response = self.login_user('joetester@se.com', 'my-new-password')

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('authdata', data)
            self.assertIn('token', data['authdata'])
            self.assertEqual(data['authdata']['email'], 'joetester@se.com')
            
        except Exception as e:
            print(f"Test failed with error: {str(e)}")
            raise


    def test_successful_logout(self):
        """
        Test logout functionality with different token scenarios:
        1. Valid token logout
        2. Already blacklisted token logout
        3. Invalid token logout
        """
        def verify_response(response, expected_status_code, expected_status, expected_message):
            """
            Helper function to verify logout response
            Args:
                response: HTTP response object
                expected_status_code: Expected HTTP status code
                expected_status: Expected status message
                expected_message: Expected response message
            """
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, expected_status_code)
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(data['status'], expected_status)
            self.assertEqual(data['message'], expected_message)
            return data

        try:
            # Test Case 1: Valid token logout
            response = self.logged_out(self.auth_token)
            verify_response(
                response, 
                200, 
                'success',
                'Successfully logged out.'
            )

            # Test Case 2: Blacklisted token logout
            response = self.logged_out(self.auth_token)
            verify_response(
                response, 
                403, 
                'fail',
                'Token is blacklisted.'
            )

            # Test Case 3: Invalid token logout
            response = self.logged_out('xxx')
            verify_response(
                response, 
                401, 
                'fail',
                'Invalid token.'
            )

        except Exception as e:
            self.fail(f"Test failed with error: {str(e)}")


if __name__ == '__main__':
    unittest.main()
