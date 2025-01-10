import json
from app import app
from app.util.test.base import BaseTestCase

class UserBaseTestCase(BaseTestCase):

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
        return app.test_client().post(
            '/u/v1/user',
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
        return app.test_client().put(
            '/u/v1/user',
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
        return app.test_client().post(
            '/u/v1/user/changepassword',
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
        return app.test_client().get(
            f'/u/v1/user/{user_id}',
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
        return app.test_client().get(
            f'/u/v1/user',
            headers={'Authorization': f'Bearer {auth_token}'}
        )  
