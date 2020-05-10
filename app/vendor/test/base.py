import json
from vms import app
from app.util.test.base import BaseTestCase

class VendorBaseTestCase(BaseTestCase):
    """ Vendor Base Tests """

     ######################
    #
    # vendor api
    #
    ######################
    @staticmethod
    def add_vendor(auth_token, vendor_name, website_name):
        return BaseTestCase.add_vendor(auth_token, vendor_name, website_name)

    @staticmethod
    def get_vendor(auth_token, vendor_id):
        return BaseTestCase.get_vendor(auth_token, vendor_id)

    @staticmethod
    def update_vendor(auth_token, vendor_id, vendor_name, website_name, status):
        return app.test_client().put(
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

    @staticmethod
    def get_all_vendor(auth_token):
        return app.test_client().get(
            '/v/v1/vendor',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )       

    @staticmethod
    def get_all_active_vendor(auth_token):
        return app.test_client().get(
            '/v/v1/vendor/active',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )               
