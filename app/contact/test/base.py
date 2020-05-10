import json
from vms import app
from app.util.test.base import BaseTestCase

class ContactBaseTestCase(BaseTestCase):
    """ Contact Base Tests """

    ######################
    #
    # contact api
    #
    ######################
    @staticmethod
    def add_contact(auth_token, contact):
        return BaseTestCase.add_contact(auth_token, contact)

    @staticmethod
    def get_contacts(auth_token, contact_id, contact_type_id):
        return app.test_client().get(
            '/c/v1/contact/{}/{}'.format(contact_id, contact_type_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )    

    @staticmethod
    def get_contact(auth_token, id):
        return app.test_client().get(
            '/c/v1/contact/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )            

    @staticmethod
    def update_contact(auth_token, contact):
        return app.test_client().put(
            '/c/v1/contact',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                id = contact.id,
                name = contact.name,
                user_by = 'jalberto'          
            )),
            content_type='application/json'
        )            

