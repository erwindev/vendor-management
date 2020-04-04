import unittest
import json

from app import db
from app.test.base import BaseTestCase


def add_vendor(self, auth_token, vendor_name, website_name):
    return self.client.post(
        '/api/v1/vendor/',
        headers=dict(
            Authorization='Bearer {}'.format(auth_token) 
        ),        
        data=json.dumps(dict(
            name=vendor_name,
            website=website_name
        )),
        content_type='application/json'
    )

def update_vendor(self, auth_token, vendor_id, vendor_name, website_name, status):
    return self.client.put(
        '/api/v1/vendor/',
        headers=dict(
            Authorization='Bearer {}'.format(auth_token) 
        ),        
        data=json.dumps(dict(
            id=vendor_id,
            name=vendor_name,
            website=website_name,
            status=status
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
        '/api/v1/vendor/',
        headers=dict(
            Authorization='Bearer {}'.format(auth_token) 
        ),        
        content_type='application/json'
    )  


class TestVendorApi(BaseTestCase):
    def test_add_vendor(self):
        """ Test for add vendor """
        auth_token, user_loggedin_data = BaseTestCase().get_token_and_loggedin_user()
        with self.client:
            # add vendor
            response = add_vendor(self, auth_token, 'Vendor 1', 'www.vendor1.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_get_all_vendor(self):
        """ Test get all vendor"""
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user()
        with self.client:
            # add vendor
            response = add_vendor(self, auth_token, 'Vendor 1', 'www.vendor1.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # get all vendor
            response = get_all_vendor(self, auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(len(data['vendorlist']) == 1)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_get_vendor(self):
        """ Test get vendor"""
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user()
        with self.client:
            # add vendor
            response = add_vendor(self, auth_token, 'Vendor X', 'www.vendorx.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # get vendor
            response = get_vendor(self, auth_token, 1)
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'Vendor X')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)            
            

    def test_update_vendor(self):
        """ Test update vendor"""
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user()
        with self.client:
            # add vendor
            response = add_vendor(self, auth_token, 'Vendor X', 'www.vendorx.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)   

            # update vendor
            response = update_vendor(self, auth_token, 1, 'Vendor Y', 'www.vendory.com', 'act')
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)    

            # get vendor
            response = get_vendor(self, auth_token, 1)
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'Vendor Y')
            self.assertTrue(data['status'] == 'act')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)                                  

if __name__ == '__main__':
    unittest.main()
