import unittest
import json
from app.notes.test.base import NotesBaseTestCase

class TestNotesApi(NotesBaseTestCase):

    def test_notes(self):
        """ Test for add notes """
        auth_token, user_loggedin_data = self.get_token_and_loggedin_user('joetester@se.com', 'test')
        
        # Create a Notes object to pass to the add_notes method
        notes = Object()
        notes.notes_id = '12345'
        notes.notes_type_id = 'TEST'
        notes.notes = 'Test Description'
        
        with self.client:
            # Use the base class method instead of direct POST
            response = self.add_notes(auth_token, notes)
            
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['message'], 'Notes successfully added.')
            self.assertEqual(data['status'], 'success')


class Object(object):
    pass

if __name__ == '__main__':
    unittest.main()
