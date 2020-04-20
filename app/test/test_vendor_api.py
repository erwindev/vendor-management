import unittest
import json

from app import db
from app.test.base import BaseTestCase


class TestVendorApi(BaseTestCase):
    def test_add_vendor(self):
        """ Test for add vendor """
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user('joetester@se.com', 'test')
        with self.client:
            # add vendor
            response = BaseTestCase().add_vendor(auth_token, 'Vendor 1', 'www.vendor1.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_get_all_vendor(self):
        """ Test get all vendor"""
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user('joetester@se.com', 'test')
        with self.client:
            # add vendor
            response = BaseTestCase().add_vendor(auth_token, 'Vendor 1', 'www.vendor1.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # get all vendor
            response = BaseTestCase().get_all_vendor(auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(len(data['vendorlist']) == 1)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_get_vendor(self):
        """ Test get vendor"""
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user('joetester@se.com', 'test')
        with self.client:
            # add vendor
            response = BaseTestCase().add_vendor(auth_token, 'Vendor X', 'www.vendorx.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # get vendor
            response = BaseTestCase().get_vendor(auth_token, 1)
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'Vendor X')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)            
            

    def test_update_vendor(self):
        """ Test update vendor"""
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user('joetester@se.com', 'test')
        with self.client:
            # add vendor
            response = BaseTestCase().add_vendor(auth_token, 'Vendor X', 'www.vendorx.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)   

            # update vendor
            response = BaseTestCase().update_vendor(auth_token, 1, 'Vendor Y', 'www.vendory.com', 'act')
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)    

            # get vendor
            response = BaseTestCase().get_vendor(auth_token, 1)
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'Vendor Y')
            self.assertTrue(data['status'] == 'act')
            self.assertTrue(data['user_by'] == 'jalberto')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)                                  

if __name__ == '__main__':
    unittest.main()
