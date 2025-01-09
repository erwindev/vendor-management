import json
from vms import app
from app.util.test.base import BaseTestCase

class ProductBaseTestCase(BaseTestCase):
    """ Product Base Tests - Contains helper methods for testing product-related endpoints """

    def add_product(self, auth_token, vendor_id, product):
        """
        Creates a new product
        Args:
            auth_token (str): JWT authentication token
            vendor_id (int): ID of the vendor
            product (Product): Product object containing details
        Returns:
            Response: Flask test client response
        """
        return super().add_product(auth_token, vendor_id, product)

    def get_product(self, auth_token, product_id):
        """
        Retrieves a specific product
        Args:
            auth_token (str): JWT authentication token
            product_id (int): ID of the product to retrieve
        Returns:
            Response: Flask test client response
        """
        return super().get_product(auth_token, product_id)

    def update_product(self, auth_token, vendor_id, product):
        """
        Updates an existing product
        Args:
            auth_token (str): JWT authentication token
            vendor_id (int): ID of the vendor
            product (Product): Product object containing updated details
        Returns:
            Response: Flask test client response
        """
        return self.client.put(
            '/p/v1/product',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                id = product.id,
                vendor_id = vendor_id,
                product_name = product.product_name,
                user_by = 'jalberto'           
            )),
            content_type='application/json'
        )    

    def get_all_product_by_vendor(self, auth_token, vendor_id):
        """
        Retrieves all products for a specific vendor
        Args:
            auth_token (str): JWT authentication token
            vendor_id (int): ID of the vendor
        Returns:
            Response: Flask test client response
        """
        return self.client.get(
            '/p/v1/product/vendor/{}'.format(vendor_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )  

    def get_all_product(self, auth_token):
        """
        Retrieves all products
        Args:
            auth_token (str): JWT authentication token
        Returns:
            Response: Flask test client response
        """
        return self.client.get(
            '/p/v1/product',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )          
