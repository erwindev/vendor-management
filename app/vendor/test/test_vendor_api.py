import unittest
import json
import datetime

from app import db
from app.util.test.base import BaseTestCase
from app.vendor.test.base import VendorBaseTestCase


class TestVendorApi(VendorBaseTestCase):
    def test_add_vendor(self):
        """ Test for add vendor """
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user('joetester@se.com', 'test')
        with self.client:
            # add vendor
            response = VendorBaseTestCase.add_vendor(auth_token, 'Vendor 1', 'www.vendor1.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_get_all_active_vendor(self):
        """ Test get all vendor"""
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user('joetester@se.com', 'test')
        with self.client:
            # add vendor
            response = VendorBaseTestCase.add_vendor(auth_token, 'Vendor 1', 'www.vendor1.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # get all vendor
            response = VendorBaseTestCase.get_all_active_vendor(auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(len(data['active_vendors']) == 1)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)            

    def test_get_all_vendor(self):
        """ Test get all vendor"""
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user('joetester@se.com', 'test')
        with self.client:
            # add vendor
            response = VendorBaseTestCase.add_vendor(auth_token, 'Vendor 1', 'www.vendor1.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # get all vendor
            response = VendorBaseTestCase.get_all_vendor(auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(len(data['vendorlist']) == 1)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_get_vendor(self):
        """ Test get vendor"""
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user('joetester@se.com', 'test')
        with self.client:
            # add vendor
            response = VendorBaseTestCase.add_vendor(auth_token, 'Vendor X', 'www.vendorx.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # get vendor
            response = VendorBaseTestCase.get_vendor(auth_token, 1)
            data = json.loads(response.data.decode())
            self.assertTrue(data['vendor']['name'] == 'Vendor X')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)      
            vendor_id = data['vendor']['id'] 

            # add contact
            contact_type_id = '1000' 
            temp_contact = Object()
            temp_contact.contact_id = vendor_id
            temp_contact.contact_type_id = contact_type_id
            temp_contact.name = "Erwin Alberto"
            temp_contact.email = "ealberto@ppeoe.com"
            temp_contact.phone1 = "904-555-4444"
            temp_contact.phone2 = "904-555-4445"
            temp_contact.street1 = "123 main st"
            temp_contact.city = "Jacksonville"
            temp_contact.state = "FL"
            temp_contact.zipcode = "32256"
            temp_contact.country = "USA"
            temp_contact.status = "Active"
            
            response = BaseTestCase.add_contact(auth_token, temp_contact)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Contact successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # add product 1
            temp_product = Object()
            temp_product.product_name = "Product 1"
            temp_product.status = "Active"
            
            response = BaseTestCase.add_product(auth_token, vendor_id, temp_product)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Product successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)          

            # add product 2
            temp_product = Object()
            temp_product.product_name = "Product 2"
            temp_product.expiration_date = datetime.date.today() + datetime.timedelta(days=365)
            temp_product.status = "Active"
            
            response = BaseTestCase.add_product(auth_token, vendor_id, temp_product)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Product successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)       

            # get vendor
            response = VendorBaseTestCase.get_vendor(auth_token, 1)
            data = json.loads(response.data.decode())
            self.assertTrue(data['vendor']['name'] == 'Vendor X')
            self.assertTrue(len(data['contacts']) == 1)
            self.assertTrue(len(data['products']) == 2)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)                              


    def test_update_vendor(self):
        """ Test update vendor"""
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user('joetester@se.com', 'test')
        with self.client:
            # add vendor
            response = BaseTestCase.add_vendor(auth_token, 'Vendor X', 'www.vendorx.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)   

            # update vendor
            response = VendorBaseTestCase.update_vendor(auth_token, 1, 'Vendor Y', 'www.vendory.com', 'act')
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)    

            # get vendor
            response = VendorBaseTestCase.get_vendor(auth_token, 1)
            data = json.loads(response.data.decode())
            self.assertTrue(data['vendor']['name'] == 'Vendor Y')
            self.assertTrue(data['vendor']['status'] == 'act')
            self.assertTrue(data['vendor']['user_by'] == 'jalberto')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)                                  



class Object(object):
    pass


if __name__ == '__main__':
    unittest.main()
