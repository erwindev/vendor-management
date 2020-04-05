import unittest
import json
import datetime

from app import db
from app.test.base import BaseTestCase


class TestProductApi(BaseTestCase):
    def test_add_product(self):
        """ Test for add product """
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user()
        with self.client:
            # add vendor
            response = BaseTestCase.add_vendor(auth_token, 'Vendor 1', 'www.vendor1.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Vendor successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)            

            # get vendor
            response = BaseTestCase.get_vendor(auth_token, 1)
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
            
            response = BaseTestCase.add_product(auth_token, temp_product)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Product successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_update_product(self):
        # add product
        # get product
        # update product
        # get product
        self.assertTrue(True)


class Object(object):
    pass

if __name__ == '__main__':
    unittest.main()
