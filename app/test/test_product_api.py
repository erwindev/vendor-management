import unittest
import json
import datetime

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

def add_product(self, auth_token, product):
    return self.client.post(
        '/api/v1/product/vendor/{}'.format(product.vendor_id),
        headers=dict(
            Authorization='Bearer {}'.format(auth_token) 
        ),        
        data=json.dumps(dict(
            product_name = product.product_name,
            department = product.department,
            budget_owner = product.budget_owner,
            product_owner = product.product_owner,
            expiration_date = str(product.expiration_date),
            payment_method = product.payment_method,
            product_type = product.product_type,
            status = product.status            
        )),
        content_type='application/json'
    )

def update_product(self, auth_token, product):
    return self.client.put(
        '/api/v1/productvendor/',
        headers=dict(
            Authorization='Bearer {}'.format(auth_token) 
        ),        
        data=json.dumps(dict(
            product_name = product.product_name,
            vendor_id = product.vendor_id,
            deparment = product.department,
            budget_owner = product.budget_owner,
            product_owner = product.product_owner,
            expiration_date = product.expiration_date,
            payment_method = product.payment_method,
            product_type = product.product_type,
            status = product.status            
        )),
        content_type='application/json'
    )    


def get_product(self, auth_token, product_id):
    return self.client.get(
        '/api/v1/product/{}'.format(product_id),
        headers=dict(
            Authorization='Bearer {}'.format(auth_token) 
        ),        
        content_type='application/json'
    )    


def get_all_product_by_vendor(self, auth_token, vendor_id):
    return self.client.get(
        '/api/v1/product/vendor/{}'.format(vendor_id),
        headers=dict(
            Authorization='Bearer {}'.format(auth_token) 
        ),        
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

class TestProductApi(BaseTestCase):
    def test_add_product(self):
        """ Test for add product """
        auth_token, user_loggedin_data = BaseTestCase().get_token_and_loggedin_user()
        with self.client:
            # add vendor
            response = add_vendor(self, auth_token, 'Vendor 1', 'www.vendor1.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)            

            # get vendor
            response = get_vendor(self, auth_token, 1)
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'Vendor 1')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)     
            vendor_id = data['id']          

            # add product
            temp_product = Object()
            temp_product.product_name = "Product 1"
            temp_product.vendor_id = vendor_id
            temp_product.department = "Department 1"
            temp_product.budget_owner = "Johnny Budget"
            temp_product.product_owner = "Johnny Owner"
            temp_product.expiration_date = datetime.date.today() + datetime.timedelta(days=365)
            temp_product.payment_method = "Credit Card"
            temp_product.product_type = "Software"
            temp_product.status = "Active"
            
            response = add_product(self, auth_token, temp_product)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Product successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    # def test_get_all_vendor(self):
    #     """ Test get all vendor"""
    #     auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user()
    #     with self.client:
    #         # add vendor
    #         response = add_vendor(self, auth_token, 'Vendor 1', 'www.vendor1.com')
    #         data = json.loads(response.data.decode())
    #         self.assertTrue(data['status'] == 'success')
    #         self.assertTrue(data['message'] == 'Vendor successfully added.')
    #         self.assertTrue(response.content_type == 'application/json')
    #         self.assertEqual(response.status_code, 201)

    #         # get all vendor
    #         response = get_all_vendor(self, auth_token)
    #         data = json.loads(response.data.decode())
    #         self.assertTrue(len(data['vendorlist']) == 1)
    #         self.assertTrue(response.content_type == 'application/json')
    #         self.assertEqual(response.status_code, 200)

    # def test_get_vendor(self):
    #     """ Test get vendor"""
    #     auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user()
    #     with self.client:
    #         # add vendor
    #         response = add_vendor(self, auth_token, 'Vendor X', 'www.vendorx.com')
    #         data = json.loads(response.data.decode())
    #         self.assertTrue(data['status'] == 'success')
    #         self.assertTrue(data['message'] == 'Vendor successfully added.')
    #         self.assertTrue(response.content_type == 'application/json')
    #         self.assertEqual(response.status_code, 201)

    #         # get vendor
    #         response = get_vendor(self, auth_token, 1)
    #         data = json.loads(response.data.decode())
    #         self.assertTrue(data['name'] == 'Vendor X')
    #         self.assertTrue(response.content_type == 'application/json')
    #         self.assertEqual(response.status_code, 200)            
            

    # def test_update_vendor(self):
    #     """ Test update vendor"""
    #     auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user()
    #     with self.client:
    #         # add vendor
    #         response = add_vendor(self, auth_token, 'Vendor X', 'www.vendorx.com')
    #         data = json.loads(response.data.decode())
    #         self.assertTrue(data['status'] == 'success')
    #         self.assertTrue(data['message'] == 'Vendor successfully added.')
    #         self.assertTrue(response.content_type == 'application/json')
    #         self.assertEqual(response.status_code, 201)   

    #         # update vendor
    #         response = update_vendor(self, auth_token, 1, 'Vendor Y', 'www.vendory.com', 'act')
    #         data = json.loads(response.data.decode())
    #         self.assertTrue(response.content_type == 'application/json')
    #         self.assertEqual(response.status_code, 201)    

    #         # get vendor
    #         response = get_vendor(self, auth_token, 1)
    #         data = json.loads(response.data.decode())
    #         self.assertTrue(data['name'] == 'Vendor Y')
    #         self.assertTrue(data['status'] == 'act')
    #         self.assertTrue(response.content_type == 'application/json')
    #         self.assertEqual(response.status_code, 200)                                  


class Object(object):
    pass

if __name__ == '__main__':
    unittest.main()
