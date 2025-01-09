import unittest
import json
import datetime
from app.notes.test.base import NotesBaseTestCase
from app.util.test.base import BaseTestCase


class TestNotesApi(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Use the class method directly
        self.auth_token, _ = self.get_token_and_loggedin_user()
        if not self.auth_token:
            raise Exception("Failed to get auth token")

    def test_notes(self):
        """ Test for add notes """
        with self.client:
            response = self.client.post(
                '/v/v1/notes',
                json={
                    'notes_id': '12345',
                    'notes_type_id': 'TEST',
                    'name': 'Test Note',
                    'description': 'Test Description',
                    'user_by': 'test@test.com'
                },
                headers={'Authorization': f'Bearer {self.auth_token}'}
            )
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['message'], 'Note successfully added.')
            self.assertEqual(data['status'], 'success')


class Object(object):
    pass

if __name__ == '__main__':
    unittest.main()
