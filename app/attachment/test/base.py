import json
from vms import app
from app.util.test.base import BaseTestCase

class AttachmentBaseTestCase(BaseTestCase):
    """ Attachment Base Tests """

    ######################
    #
    # attachment api
    #
    ######################
    @staticmethod
    def add_attachment(auth_token, attachment):
        return app.test_client().post(
            '/a/api/v1/attachment',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                attachment_id = attachment.attachment_id,
                attachment_type_id = attachment.attachment_type_id,
                name = attachment.name,
                link = attachment.link,
                description = attachment.description,
                user_by = 'ealberto'          
            )),
            content_type='application/json'
        )        

    @staticmethod
    def get_all_attachments(auth_token, attachmment_id, attachment_type_id):
        return app.test_client().get(
            '/a/api/v1/attachment/{}/{}'.format(attachmment_id, attachment_type_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )    

    @staticmethod
    def get_attachment(auth_token, id):
        return app.test_client().get(
            '/a/api/v1/attachment/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )            

    @staticmethod
    def update_attachment(auth_token, id, attachment):
        return app.test_client().put(
            '/a/api/v1/attachment/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                name = attachment.name,
                user_by = 'jalberto'           
            )),
            content_type='application/json'
        )                    

    @staticmethod
    def delete_attachment(auth_token, id):
        return app.test_client().delete(
            '/a/api/v1/attachment/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'   
        )  
