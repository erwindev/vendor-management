import unittest
import json
from flask_testing import TestCase

from app import db
from vms import app
from app.vendor.models.user import User


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):        
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        user = User()
        user.firstname = 'joe'
        user.lastname = 'tester'
        user.email = 'joetester@se.com'
        user.set_password('test')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ######################
    #
    # auth api
    #
    ######################
    @staticmethod
    def login_user(email, password):
        return app.test_client().post(
            '/api/v1/auth/login',
            data=json.dumps(dict(
                email=email,
                password=password
            )),
            content_type='application/json'
        )

    @staticmethod
    def get_token_and_loggedin_user(email, password):
        response = BaseTestCase.login_user(email, password)
        data = json.loads(response.data.decode())
        user_loggedin_data = json.loads(response.data.decode())                  
        auth_token = user_loggedin_data['authdata']['token']     
        return auth_token, user_loggedin_data['authdata']  

    @staticmethod
    def logged_out(auth_token):
        return app.test_client().post(
            '/api/v1/auth/logout',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )  

    ######################
    #
    # user api
    #
    ######################
    @staticmethod
    def register_user(auth_token):
        return app.test_client().post(
            '/api/v1/user/',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                email='ealberto-test@me.com',
                firstname='erwin',
                lastname='alberto',
                password='test'
            )),
            content_type='application/json'
        )

    @staticmethod
    def update_user(auth_token, id, firstname, lastname, status):
        return app.test_client().put(
            '/api/v1/user/',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                id=id,
                firstname=firstname,
                lastname=lastname,
                status=status
            )),
            content_type='application/json'
        )

    @staticmethod
    def change_password(auth_token, id, password, new_password):
        return app.test_client().post(
            '/api/v1/user/changepassword',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                id=id,
                password=password,
                newpassword=new_password
            )),
            content_type='application/json'
        )                

    @staticmethod
    def get_user(auth_token, id):
        return app.test_client().get(
            '/api/v1/user/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )    

    @staticmethod
    def get_all_user(auth_token):
        return app.test_client().get(
            '/api/v1/user/',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )  


    ######################
    #
    # vendor api
    #
    ######################
    @staticmethod
    def add_vendor(auth_token, vendor_name, website_name):
        return app.test_client().post(
            '/api/v1/vendor/',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                name=vendor_name,
                website=website_name,
                status="Active",
                user_by = '1' 
            )),
            content_type='application/json'
        )

    @staticmethod
    def get_vendor(auth_token, vendor_id):
        return app.test_client().get(
            '/api/v1/vendor/{}'.format(vendor_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )    

    @staticmethod
    def update_vendor(auth_token, vendor_id, vendor_name, website_name, status):
        return app.test_client().put(
            '/api/v1/vendor/',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                id=vendor_id,
                name=vendor_name,
                website=website_name,
                status=status,
                user_by = 'jalberto' 
            )),
            content_type='application/json'
        )     

    @staticmethod
    def get_all_vendor(auth_token):
        return app.test_client().get(
            '/api/v1/vendor/',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )       

    @staticmethod
    def get_all_active_vendor(auth_token):
        return app.test_client().get(
            '/api/v1/vendor/active',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )               


    ######################
    #
    # product api
    #
    ######################
    @staticmethod
    def add_product(auth_token, vendor_id, product):
        return app.test_client().post(
            '/api/v1/product/vendor/{}'.format(vendor_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                product_name = product.product_name,
                status = product.status,
                user_by = 'ealberto'            
            )),
            content_type='application/json'
        )        

    @staticmethod
    def update_product(auth_token, vendor_id, product):
        return app.test_client().put(
            '/api/v1/product/vendor/{}'.format(vendor_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                id = product.id,
                product_name = product.product_name,
                user_by = 'jalberto'           
            )),
            content_type='application/json'
        )    


    @staticmethod
    def get_product(auth_token, product_id):
        return app.test_client().get(
            '/api/v1/product/{}'.format(product_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )    


    @staticmethod
    def get_all_product_by_vendor(auth_token, vendor_id):
        return app.test_client().get(
            '/api/v1/product/vendor/{}'.format(vendor_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )  


    ######################
    #
    # contact api
    #
    ######################
    @staticmethod
    def add_contact(auth_token, contact):
        return app.test_client().post(
            '/api/v1/contact/',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                contact_id = contact.contact_id,
                contact_type_id = contact.contact_type_id,
                name = contact.name,
                email = contact.email,
                phone1 = contact.phone1,
                phone2 = contact.phone2,
                street1 = contact.street1,
                city = contact.city,
                state = contact.state,
                country = contact.country,
                zipcode = contact.zipcode,
                status = contact.status,
                user_by = 'ealberto'            
            )),
            content_type='application/json'
        )        

    @staticmethod
    def get_contacts(auth_token, contact_id, contact_type_id):
        return app.test_client().get(
            '/api/v1/contact/{}/{}'.format(contact_id, contact_type_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )    

    @staticmethod
    def get_contact(auth_token, id):
        return app.test_client().get(
            '/api/v1/contact/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )            

    @staticmethod
    def update_contact(auth_token, contact):
        return app.test_client().put(
            '/api/v1/contact/',
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

    ######################
    #
    # notes api
    #
    ######################
    @staticmethod
    def add_notes(auth_token, notes):
        return app.test_client().post(
            '/api/v1/notes/',
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
            '/api/v1/notes/{}/{}'.format(notes_id, notes_type_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )    

    @staticmethod
    def get_notes(auth_token, id):
        return app.test_client().get(
            '/api/v1/notes/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )            

    @staticmethod
    def update_notes(auth_token, id, notes):
        return app.test_client().put(
            '/api/v1/notes/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                notes = notes.notes,
                user_by = 'jalberto'           
            )),
            content_type='application/json'
        )            

    ######################
    #
    # attachment api
    #
    ######################
    @staticmethod
    def add_attachment(auth_token, attachment):
        return app.test_client().post(
            '/api/v1/attachment/',
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
            '/api/v1/attachment/{}/{}'.format(attachmment_id, attachment_type_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )    

    @staticmethod
    def get_attachment(auth_token, id):
        return app.test_client().get(
            '/api/v1/attachment/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )            

    @staticmethod
    def update_attachment(auth_token, id, attachment):
        return app.test_client().put(
            '/api/v1/attachment/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                name = attachment.name,
                user_by = 'jalberto'           
            )),
            content_type='application/json'
        )                    