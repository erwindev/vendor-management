import json
from vms import app
from app.util.test.base import BaseTestCase

class UserBaseTestCase(BaseTestCase):
    """
    Base test case class for user-related API endpoints.
    Provides helper methods for common user operations in tests.
    """
    def setUp(self):
        """
        Initialize test environment with Flask test client and base URL.
        Called before each test method.
        """
        self.app = app
        self.client = self.app.test_client()
        self.base_url = 'http://localhost:5000'  # Base URL for API endpoints
        
    ######################
    # User API Methods
    # Helper methods for testing user-related endpoints
    ######################
    
    def register_user(self, auth_token):
        """
        Register a new user with test credentials.
        
        Args:
            auth_token (str): Authentication token for the request
            
        Returns:
            Response: Flask response object from the registration request
        """
        url = f'{self.base_url}/u/v1/user'
        
        return self.client.post(
            url,
            headers={
                'Authorization': f'Bearer {auth_token}',
                'Content-Type': 'application/json'
            },
            json={
                'email': 'ealberto-test@me.com',
                'firstname': 'erwin',
                'lastname': 'alberto',
                'password': 'test'
            }
        )

    def update_user(self, auth_token, id, firstname, lastname, status):
        """
        Update an existing user's information.
        """
        return self.client.put(
            f'{self.base_url}/u/v1/user',
            headers={
                'Authorization': f'Bearer {auth_token}',
                'Content-Type': 'application/json'
            },
            json={
                'id': id,
                'firstname': firstname,
                'lastname': lastname,
                'status': status
            }
        )

    def change_password(self, auth_token, id, password, new_password):
        """
        Change a user's password.
        """
        return self.client.post(
            f'{self.base_url}/u/v1/user/changepassword',
            headers={
                'Authorization': f'Bearer {auth_token}',
                'Content-Type': 'application/json'
            },
            json={
                'id': id,
                'password': password,
                'newpassword': new_password
            }
        )

    def get_user(self, auth_token, user_id):
        """
        Retrieve a specific user's information.
        
        Args:
            auth_token (str): Authentication token for the request
            user_id (int): ID of the user to retrieve
            
        Returns:
            Response: Flask response object containing user data
        """
        url = f'{self.base_url}/u/v1/user/{user_id}'
        return self.client.get(
            url,
            headers={'Authorization': f'Bearer {auth_token}'}
        )    

    def get_all_user(self, auth_token):
        """
        Retrieve information for all users.
        
        Args:
            auth_token (str): Authentication token for the request
            
        Returns:
            Response: Flask response object containing all users' data
        """
        return self.client.get(
            f'{self.base_url}/u/v1/user',
            headers={'Authorization': f'Bearer {auth_token}'}
        )  
