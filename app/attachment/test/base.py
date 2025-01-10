import json
from app.util.test.base import BaseTestCase

class AttachmentBaseTestCase(BaseTestCase):
    """ Attachment Base Tests """

    def add_attachment(self, auth_token, attachment):
        """
        Creates a new attachment.
        
        Args:
            auth_token (str): JWT authentication token
            attachment (Attachment): Attachment object containing details
            
        Returns:
            Response: Flask test client response
        """
        return self.client.post(
            '/a/v1/attachment',
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

    def get_all_attachments(self, auth_token, attachment_id, attachment_type_id):
        """
        Retrieves all attachments for a specific attachment_id and type.
        
        Args:
            auth_token (str): JWT authentication token
            attachment_id (str): Identifier for the attachment
            attachment_type_id (str): Type identifier for the attachment
            
        Returns:
            Response: Flask test client response
        """
        return self.client.get(
            '/a/v1/attachment/{}/{}'.format(attachment_id, attachment_type_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )    

    def get_attachment(self, auth_token, id):
        """
        Retrieves a specific attachment by ID.
        
        Args:
            auth_token (str): JWT authentication token
            id (str): Unique identifier of the attachment
            
        Returns:
            Response: Flask test client response
        """
        return self.client.get(
            '/a/v1/attachment/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )            

    def update_attachment(self, auth_token, id, attachment):
        """
        Updates an existing attachment.
        
        Args:
            auth_token (str): JWT authentication token
            id (str): Unique identifier of the attachment
            attachment (Attachment): Attachment object with updated details
            
        Returns:
            Response: Flask test client response
        """
        return self.client.put(
            '/a/v1/attachment/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                name = attachment.name,
                user_by = 'jalberto'           
            )),
            content_type='application/json'
        )                    

    def delete_attachment(self, auth_token, id):
        """
        Deletes a specific attachment.
        
        Args:
            auth_token (str): JWT authentication token
            id (str): Unique identifier of the attachment to delete
            
        Returns:
            Response: Flask test client response
        """
        return self.client.delete(
            '/a/v1/attachment/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'   
        )  
