import json
from vms import app
from app.util.test.base import BaseTestCase

class ContactBaseTestCase(BaseTestCase):
    """ Contact Base Tests - Contains helper methods for testing contact-related endpoints """

    def add_contact(self, auth_token, contact):
        """
        Creates a new contact
        Args:
            auth_token (str): JWT authentication token
            contact (Contact): Contact object containing contact details
        Returns:
            Response: Flask test client response
        """
        # Use super() with self to properly call the parent class's instance method
        return super(ContactBaseTestCase, self).add_contact(auth_token, contact)

    def get_contacts(self, auth_token, contact_id, contact_type_id):
        """
        Retrieves contacts by contact ID and type
        Args:
            auth_token (str): JWT authentication token
            contact_id (int): ID of the contact
            contact_type_id (int): Type ID of the contact
        Returns:
            Response: Flask test client response
        """
        return self.client.get(
            '/c/v1/contact/{}/{}'.format(contact_id, contact_type_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )    

    def get_contact(self, auth_token, id):
        """
        Retrieves a specific contact's information
        Args:
            auth_token (str): JWT authentication token
            id (int): ID of the contact to retrieve
        Returns:
            Response: Flask test client response
        """
        return self.client.get(
            '/c/v1/contact/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )            

    def update_contact(self, auth_token, contact):
        """
        Updates an existing contact's information
        Args:
            auth_token (str): JWT authentication token
            contact (Contact): Contact object containing updated details
        Returns:
            Response: Flask test client response
        """
        return self.client.put(
            '/c/v1/contact',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                id = contact.id,
                name = contact.name,
                user_by = 'jalberto'          
            )),
            content_type='application/json'
        )            

