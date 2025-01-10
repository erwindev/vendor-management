import json
from app.util.test.base import BaseTestCase

class NotesBaseTestCase(BaseTestCase):
    """ Notes Base Tests """

    def add_notes(self, auth_token, notes):
        return self.client.post(
            '/n/v1/notes',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                notes_id = notes.notes_id,
                notes_type_id = notes.notes_type_id,
                notes = notes.notes,
                user_by = 'ealberto'          
            )),
            content_type='application/json'
        )        

    def get_all_notes(self, auth_token, notes_id, notes_type_id):
        return self.client.get(
            '/n/v1/notes/{}/{}'.format(notes_id, notes_type_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )    

    def get_notes(self, auth_token, id):
        return self.client.get(
            '/n/v1/notes/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )            

    def update_notes(self, auth_token, id, notes):
        return self.client.put(
            '/n/v1/notes/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                notes = notes.notes,
                user_by = 'jalberto'           
            )),
            content_type='application/json'
        )            

    def delete_notes(self, auth_token, id):
        return self.client.delete(
            '/n/v1/notes/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json' 
        )         
