import unittest
import json
from app.attachment.test.base import AttachmentBaseTestCase

class TestAttachmentApi(AttachmentBaseTestCase):
    def test_attachment(self):
        """ Test for add attachment """
        auth_token, user_loggedin_data = self.get_token_and_loggedin_user('joetester@se.com', 'test')
        with self.client:

            attachment_type_id = '1000' 

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

            # add attachment
            temp_attachment = Object()
            temp_attachment.attachment_id = vendor_id
            temp_attachment.attachment_type_id = attachment_type_id
            temp_attachment.name = 'Contract link'
            temp_attachment.description = 'This is a sample link'
            temp_attachment.link = 'http://link.com'
            
            response = self.add_attachment(auth_token, temp_attachment)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Attachment successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # get all attachment by vendor
            response = self.get_all_attachments(auth_token, vendor_id, attachment_type_id)
            data = json.loads(response.data.decode())
            attachment_id = data["attachmentlist"][0]['id']

            # get attachment
            response = self.get_attachment(auth_token, attachment_id)
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'Contract link')
            self.assertTrue(data['description'] == 'This is a sample link')
            self.assertTrue(data['link'] == 'http://link.com')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)      

            # update attachment
            another_temp_attachment = Object()
            another_temp_attachment.name = 'Contract linkxxxxx'
            response = self.update_attachment(auth_token, attachment_id, another_temp_attachment)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)           

            # get updated attachment
            response = self.get_attachment(auth_token, attachment_id)
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'Contract linkxxxxx')
            self.assertTrue(data['user_by'] == 'jalberto')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)            

            # delete attachment
            response = self.delete_attachment(auth_token, attachment_id)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)                           


class Object(object):
    pass

if __name__ == '__main__':
    unittest.main()
