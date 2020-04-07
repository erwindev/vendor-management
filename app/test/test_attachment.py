import unittest
import json
import datetime

from app import db
from app.test.base import BaseTestCase


class TestAttachmentApi(BaseTestCase):
    def test_attachment(self):
        """ Test for add attachment """
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user()
        with self.client:

            attachment_type_id = '1000' 

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

            # add attachment
            temp_attachment = Object()
            temp_attachment.attachment_id = vendor_id
            temp_attachment.attachment_type_id = attachment_type_id
            temp_attachment.name = 'Contract link'
            temp_attachment.description = 'This is a sample link'
            temp_attachment.link = 'http://link.com'
            
            response = BaseTestCase.add_attachment(auth_token, temp_attachment)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Attachment successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # get all attachment by vendor
            response = BaseTestCase.get_all_attachments(auth_token, vendor_id, attachment_type_id)
            data = json.loads(response.data.decode())
            attachment_id = data["attachmentlist"][0]['id']

            # get attachment
            response = BaseTestCase.get_attachment(auth_token, attachment_id)
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'Contract link')
            self.assertTrue(data['description'] == 'This is a sample link')
            self.assertTrue(data['link'] == 'http://link.com')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)      

            # update attachment
            another_temp_attachment = Object()
            another_temp_attachment.name = 'Contract linkxxxxx'
            response = BaseTestCase.update_attachment(auth_token, attachment_id, another_temp_attachment)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)           

            # get updated attachment
            response = BaseTestCase.get_attachment(auth_token, attachment_id)
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'Contract linkxxxxx')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)                       


class Object(object):
    pass

if __name__ == '__main__':
    unittest.main()
