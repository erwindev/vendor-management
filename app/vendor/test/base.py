import json
from vms import app
from app.util.test.base import BaseTestCase

class VendorBaseTestCase(BaseTestCase):
    """ Vendor Base Tests - Contains helper methods for testing vendor-related endpoints """

    def add_vendor(self, auth_token, vendor_name, website_name):
        """
        Creates a new vendor
        Args:
            auth_token (str): JWT authentication token
            vendor_name (str): Name of the vendor
            website_name (str): Vendor's website URL
        Returns:
            Response: Flask test client response
        """
        return super().add_vendor(auth_token, vendor_name, website_name)

    def get_vendor(self, auth_token, vendor_id):
        """
        Retrieves a specific vendor
        Args:
            auth_token (str): JWT authentication token
            vendor_id (int): ID of the vendor to retrieve
        Returns:
            Response: Flask test client response
        """
        return super().get_vendor(auth_token, vendor_id)

    def update_vendor(self, auth_token, vendor_id, vendor_name, website_name, status):
        """
        Updates an existing vendor's information
        Args:
            auth_token (str): JWT token for authentication
            vendor_id (int): ID of the vendor to update
            vendor_name (str): New name for the vendor
            website_name (str): New website URL
            status (str): Updated status of the vendor
        Returns:
            Response: Flask test client response
        """
        return self.client.put(
            '/v/v1/vendor',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                id=vendor_id,
                name=vendor_name,
                website=website_name,
                status=status,
                user_by = 'jalberto' 
            )),
            content_type='application/json'
        )     

    def get_all_vendor(self, auth_token):
        """
        Retrieves a list of all vendors regardless of status
        Args:
            auth_token (str): JWT token for authentication
        Returns:
            Response: Flask test client response with list of vendors
        """
        return self.client.get(
            '/v/v1/vendor',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )       

    def get_all_active_vendor(self, auth_token):
        """
        Retrieves a list of only active vendors
        Args:
            auth_token (str): JWT token for authentication
        Returns:
            Response: Flask test client response with list of active vendors
        """
        return self.client.get(
            '/v/v1/vendor/active',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )               
