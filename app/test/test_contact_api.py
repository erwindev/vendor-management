import unittest
import json
import datetime

from app import db
from app.test.base import BaseTestCase


class TestContactApi(BaseTestCase):
    def test_contact(self):
        """ Test for add contact """
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user('joetester@se.com', 'test')
        with self.client:

            contact_type_id = '1000' 

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
            self.assertTrue(data['vendor']['name'] == 'Vendor 1')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)     
            vendor_id = data['vendor']['id']          

            # add contact
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

            # get all contacts by vendor
            response = BaseTestCase.get_contacts(auth_token, vendor_id, contact_type_id)
            data = json.loads(response.data.decode())
            contact_id = data["contactlist"][0]['id']

            # get contact
            response = BaseTestCase.get_contact(auth_token, contact_id)
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'Erwin Alberto')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)      

            # update contact
            another_temp_contact = Object()
            another_temp_contact.name = 'Julian Alberto'
            response = BaseTestCase.update_contact(auth_token, contact_id, another_temp_contact)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)           

            # get updated contact
            response = BaseTestCase.get_contact(auth_token, contact_id)
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'Julian Alberto')
            self.assertTrue(data['user_by'] == 'jalberto')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)                       


class Object(object):
    pass

if __name__ == '__main__':
    unittest.main()
