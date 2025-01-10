import unittest
import json
from app.product.test.base import ProductBaseTestCase
from app.util.constants import TEST_USER_EMAIL, TEST_USER_PASSWORD

class TestProductApi(ProductBaseTestCase):
    def test_add_product(self):
        """ Test for add product """
        auth_token, user_loggedin_data = self.get_token_and_loggedin_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        with self.client:
            # add vendor
            response = self.add_vendor(auth_token, 'Vendor 1', 'www.vendor1.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)            

            # get vendor
            response = self.get_vendor(auth_token, 1)
            data = json.loads(response.data.decode())
            self.assertTrue(data['vendor']['name'] == 'Vendor 1')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)     
            vendor_id = data['vendor']['id']          

            # add product
            temp_product = Object()
            temp_product.product_name = "Product 1"
            temp_product.vendor_id = vendor_id
            temp_product.status = "Active"
            response = self.add_product(auth_token, vendor_id, temp_product)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Product successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # get all products by vendor
            response = self.get_all_product_by_vendor(auth_token, vendor_id)
            data = json.loads(response.data.decode())
            product_id = data["productlist"][0]['id']

            # get product 1
            response = self.get_product(auth_token, product_id)
            data = json.loads(response.data.decode())
            self.assertTrue(data['product_name'] == 'Product 1')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)       

            # add product
            temp_product = Object()
            temp_product.product_name = "Product 2"
            temp_product.vendor_id = vendor_id
            temp_product.status = "Active"   
            response = self.add_product(auth_token, vendor_id, temp_product)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Product successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)            

            # get all product
            response = self.get_all_product(auth_token)
            data = json.loads(response.data.decode())
            self.assertTrue(len(data['productlist']) == 2)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)                     

            product_list = data['productlist']
            for product in product_list:
                 self.assertTrue(product['vendor_id'] == '1')


    def test_update_product(self):
        """ Test for update product """
        auth_token, user_loggedin_data = self.get_token_and_loggedin_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        with self.client:        
            # add vendor
            response = self.add_vendor(auth_token, 'Vendor 1', 'www.vendor1.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)            

            # get vendor
            response = self.get_vendor(auth_token, 1)
            data = json.loads(response.data.decode())
            self.assertTrue(data['vendor']['name'] == 'Vendor 1')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)     
            vendor_id = data['vendor']['id']      

            # add product 1
            temp_product = Object()
            temp_product.product_name = "Product 1"
            temp_product.status = "Active"
            
            response = self.add_product(auth_token, vendor_id, temp_product)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Product successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)          

            # add product 2
            temp_product = Object()
            temp_product.product_name = "Product 2"
            temp_product.status = "Active"
            
            response = self.add_product(auth_token, vendor_id, temp_product)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Product successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)               

            # get all products by vendor
            response = self.get_all_product_by_vendor(auth_token, vendor_id)
            data = json.loads(response.data.decode())
            product_id = data["productlist"][0]['id']

            # get product 1
            response = self.get_product(auth_token, product_id)
            data = json.loads(response.data.decode())
            self.assertTrue(data['product_name'] == 'Product 1')
            self.assertTrue(data['vendor_id'] == '1')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)         

            # update product
            another_temp_product = Object()
            another_temp_product.id = product_id
            another_temp_product.product_name = 'Product xxxxx'
            response = self.update_product(auth_token, vendor_id, another_temp_product)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)                     

            # get product 1
            response = self.get_product(auth_token, product_id)
            data = json.loads(response.data.decode())
            self.assertTrue(data['product_name'] == 'Product xxxxx')
            self.assertTrue(data['user_by'] == 'jalberto')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)                           



class Object(object):
    pass

if __name__ == '__main__':
    unittest.main()
