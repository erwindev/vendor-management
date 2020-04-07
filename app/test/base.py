import unittest
import json
from flask_testing import TestCase

from app import db
from application import app
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
        user.username = 'joe.tester'
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
    def login_user():
        return app.test_client().post(
            '/api/v1/auth/login',
            data=json.dumps(dict(
                username='joe.tester',
                password='test'
            )),
            content_type='application/json'
        )

    @staticmethod
    def get_token_and_loggedin_user():
        response = BaseTestCase.login_user()
        data = json.loads(response.data.decode())
        user_loggedin_data = json.loads(response.data.decode())                  
        auth_token = user_loggedin_data['Authorization']      
        return auth_token, user_loggedin_data  

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
                username='ealberto-test',
                firstname='erwin',
                lastname='alberto',
                password='test'
            )),
            content_type='application/json'
        )

    @staticmethod
    def update_user(auth_token, user_id, firstname, lastname, status):
        return app.test_client().put(
            '/api/v1/user/',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                id=user_id,
                firstname=firstname,
                lastname=lastname,
                status=status
            )),
            content_type='application/json'
        )        

    @staticmethod
    def get_user(auth_token, user_id):
        return app.test_client().get(
            '/api/v1/user/{}'.format(user_id),
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
                status="active"
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
                status=status
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
                department = product.department,
                budget_owner = product.budget_owner,
                product_owner = product.product_owner,
                expiration_date = str(product.expiration_date),
                payment_method = product.payment_method,
                product_type = product.product_type,
                status = product.status            
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
                product_name = product.product_name           
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
                status = contact.status            
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
    def update_contact(auth_token, id, contact):
        return app.test_client().put(
            '/api/v1/contact/{}'.format(id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                name = contact.name           
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
                notes = notes.notes          
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
                notes = notes.notes           
            )),
            content_type='application/json'
        )            