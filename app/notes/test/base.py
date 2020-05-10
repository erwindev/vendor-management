import json
from vms import app
from app.util.test.base import BaseTestCase

class NotesBaseTestCase(BaseTestCase):
    """ Notes Base Tests """

    ######################
    #
    # notes api
    #
    ######################
    @staticmethod
    def add_notes(auth_token, notes):
        return app.test_client().post(
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

    @staticmethod
    def get_all_notes(auth_token, notes_id, notes_type_id):
        return app.test_client().get(
            '/n/v1/notes/{}/{}'.format(notes_id, notes_type_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )    

    @staticmethod
    def get_notes(auth_token, id):
        return app.test_client().get(
            '/n/v1/notes/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )            

    @staticmethod
    def update_notes(auth_token, id, notes):
        return app.test_client().put(
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

    @staticmethod
    def delete_notes(auth_token, id):
        return app.test_client().delete(
            '/n/v1/notes/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json' 
        )         
