import unittest
import json
import datetime

from app import db
from app.test.base import BaseTestCase


class TestNotesApi(BaseTestCase):
    def test_notes(self):
        """ Test for add notes """
        auth_token, user_loggedin_data = BaseTestCase.get_token_and_loggedin_user()
        with self.client:

            notes_type_id = '1000' 

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

            # add notes
            temp_notes = Object()
            temp_notes.notes_id = vendor_id
            temp_notes.notes_type_id = notes_type_id
            temp_notes.notes = "This is my notes"
            
            response = BaseTestCase.add_notes(auth_token, temp_notes)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Notes successfully added.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # get all notes by vendor
            response = BaseTestCase.get_all_notes(auth_token, vendor_id, notes_type_id)
            data = json.loads(response.data.decode())
            notes_id = data["noteslist"][0]['id']

            # get notes
            response = BaseTestCase.get_notes(auth_token, notes_id)
            data = json.loads(response.data.decode())
            self.assertTrue(data['notes'] == 'This is my notes')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)      

            # update notes
            another_temp_notes = Object()
            another_temp_notes.notes = 'I updated this note'
            response = BaseTestCase.update_notes(auth_token, notes_id, another_temp_notes)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)           

            # get updated notes
            response = BaseTestCase.get_notes(auth_token, notes_id)
            data = json.loads(response.data.decode())
            self.assertTrue(data['notes'] == 'I updated this note')
            self.assertTrue(data['user_by'] == 'jalberto')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)                       


class Object(object):
    pass

if __name__ == '__main__':
    unittest.main()
