import json
from vms import app
from app.util.test.base import BaseTestCase

class ProductBaseTestCase(BaseTestCase):
    """ Product Base Tests """

   ######################
    #
    # product api
    #
    ######################
    @staticmethod
    def add_product(auth_token, vendor_id, product):
        return BaseTestCase.add_product(auth_token, vendor_id, product)        

    @staticmethod
    def update_product(auth_token, vendor_id, product):
        return app.test_client().put(
            '/p/api/v1/product',
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

    @staticmethod
    def get_product(auth_token, product_id):
        return BaseTestCase.get_product(auth_token, product_id)    

    @staticmethod
    def get_all_product_by_vendor(auth_token, vendor_id):
        return app.test_client().get(
            '/p/api/v1/product/vendor/{}'.format(vendor_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )  

    @staticmethod
    def get_all_product(auth_token):
        return app.test_client().get(
            '/p/api/v1/product',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )          
