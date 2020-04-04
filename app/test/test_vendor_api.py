import unittest
import json

from app import db
from app.test.base import BaseTestCase


def add_vendor(self, auth_token):
    return self.client.post(
        '/api/v1/vendor/',
        headers=dict(
            Authorization='Bearer {}'.format(auth_token) 
        ),        
        data=json.dumps(dict(
            name='Vendor 1',
            website='www.vendor1.com'
        )),
        content_type='application/json'
    )


def get_vendor(self, auth_token, vendor_id):
    return self.client.get(
        '/api/v1/vendor/{}'.format(vendor_id),
        headers=dict(
            Authorization='Bearer {}'.format(auth_token) 
        ),        
        content_type='application/json'
    )    


def get_all_vendor(self, auth_token):
    return self.client.get(
        '/api/v1/vendor/'.format(vendor_id),
        headers=dict(
            Authorization='Bearer {}'.format(auth_token) 
        ),        
        content_type='application/json'
    )  


class TestVendorApi(BaseTestCase):
    def test_add_vendor(self):
        """ Test for add vendor """
        with self.client:
            auth_token, user_loggedin_data = BaseTestCase().get_token_and_loggedin_user()
            response = add_vendor(self, auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def get_all_vendor(self):
        """ Test get vendor"""
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user()
        with self.client:
            response = get_all_vendor(self, auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(len(data) == 1)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            

if __name__ == '__main__':
    unittest.main()
