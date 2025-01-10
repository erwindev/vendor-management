import json
from flask_testing import TestCase

from app import db, app
from app.user.models.user import User

class BaseTestCase(TestCase):
    """ Base Tests - Contains core testing functionality and common helper methods """

    def create_app(self):      
        # Returns the Flask application instance for testing
        return app

    def setUp(self):
        # Set up test database and create a test user before each test
        db.create_all()
        user = User()
        user.firstname = 'joe'
        user.lastname = 'tester'
        user.email = 'joetester@se.com'
        user.set_password('test')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        # Clean up test database after each test
        db.session.remove()
        db.drop_all()

    ######################
    # Authentication API Methods
    ######################
    def login_user(self, email, password):
        """
        Simulates a user login request
        Args:
            email (str): User's email address
            password (str): User's password
        Returns:
            Response: Flask test client response
        """
        return app.test_client().post(
            '/u/v1/auth/login',
            data=json.dumps(dict(
                email=email,
                password=password
            )),
            content_type='application/json'
        )

    def get_token_and_loggedin_user(self, email='test@test.com', password='test123'):
        """
        Helper method to get authentication token and user data
        Args:
            email (str, optional): User's email. Defaults to 'test@test.com'
            password (str, optional): User's password. Defaults to 'test123'
        Returns:
            tuple: (auth_token, user_data) or (None, None) if login fails
        """
        with self.client as client:
            resp = client.post(
                '/u/v1/auth/login',
                json={
                    'email': email,
                    'password': password
                },
                mimetype='application/json'
            )
            print("------resp-----")
            print(resp)
            if resp.status_code == 200:
                response_data = json.loads(resp.data)
                auth_token = response_data['authdata']['token']
                return auth_token, response_data
            else:
                print(f"Login failed with status code: {resp.status_code}")
                print(f"Response: {resp.data}")
                return None, None

    def logged_out(self, auth_token):
        """
        Simulates a user logout request
        Args:
            auth_token (str): JWT authentication token
        Returns:
            Response: Flask test client response
        """
        return app.test_client().post(
            '/u/v1/auth/logout',
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )  

    ######################
    # Vendor API Methods
    ######################
    def add_vendor(self, auth_token, vendor_name, website_name):
        """
        Creates a new vendor
        Args:
            auth_token (str): JWT authentication token
            vendor_name (str): Name of the vendor
            website_name (str): Vendor's website URL
        Returns:
            Response: Flask test client response
        """
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

    def get_vendor(self, auth_token, vendor_id):
        """
        Retrieves a specific vendor's information
        Args:
            auth_token (str): JWT authentication token
            vendor_id (int): ID of the vendor to retrieve
        Returns:
            Response: Flask test client response
        """
        return app.test_client().get(
            '/v/v1/vendor/{}'.format(vendor_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )    

    ######################
    # Product API Methods
    ######################
    def add_product(self, auth_token, vendor_id, product):
        """
        Creates a new product
        Args:
            auth_token (str): JWT authentication token
            vendor_id (int): ID of the vendor who owns the product
            product (Product): Product object containing product details
        Returns:
            Response: Flask test client response
        """
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

    def get_product(self, auth_token, product_id):
        """
        Retrieves a specific product's information
        Args:
            auth_token (str): JWT authentication token
            product_id (int): ID of the product to retrieve
        Returns:
            Response: Flask test client response
        """
        return app.test_client().get(
            '/p/v1/product/{}'.format(product_id),
            headers=dict(
                Authorization='Bearer {}'.format(auth_token) 
            ),        
            content_type='application/json'
        )    

    ######################
    # Contact API Methods
    ######################
    def add_contact(self, auth_token, contact):
        """
        Creates a new contact
        Args:
            auth_token (str): JWT authentication token
            contact (Contact): Contact object containing contact details
        Returns:
            Response: Flask test client response
        """
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
