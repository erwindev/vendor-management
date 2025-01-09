import os
import unittest
import json
from flask_testing import TestCase

from app import create_app
from app import db
from app.user.models.user import User

app = create_app()

class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):      
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
            '/u/v1/auth/login',
            data=json.dumps(dict(
                email=email,
                password=password
            )),
            content_type='application/json'
        )

    def get_token_and_loggedin_user(self, email='test@test.com', password='test123'):
        with self.client as client:
            resp = client.post(
                '/u/v1/auth/login',
                json={
                    'email': email,
                    'password': password
                },
                mimetype='application/json'
            )
            if resp.status_code == 200:
                response_data = json.loads(resp.data)
                auth_token = response_data['authdata']['token']
                return auth_token, response_data
            else:
                print(f"Login failed with status code: {resp.status_code}")
                print(f"Response: {resp.data}")
                return None, None

    @staticmethod
    def logged_out(auth_token):
        return app.test_client().post(
            '/u/v1/auth/logout',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )  

    ######################
    #
    # base vendor api
    #
    ######################
    @staticmethod
    def add_vendor(auth_token, vendor_name, website_name):
        return app.test_client().post(
            '/v/v1/vendor',
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
            '/v/v1/vendor/{}'.format(vendor_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )    

   ######################
    #
    # base product api
    #
    ######################
    @staticmethod
    def add_product(auth_token, vendor_id, product):
        return app.test_client().post(
            '/p/v1/product',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            data=json.dumps(dict(
                product_name = product.product_name,
                vendor_id = vendor_id,
                status = product.status,
                user_by = 'ealberto'            
            )),
            content_type='application/json'
        )        

    @staticmethod
    def get_product(auth_token, product_id):
        return app.test_client().get(
            '/p/v1/product/{}'.format(product_id),
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
            '/c/v1/contact',
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
