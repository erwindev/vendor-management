import unittest
import logging
from app import create_app
from app.util.test.base import BaseTestCase

class TestApp():
    def suite(self):
        # Initialize base test cases and set up test environment
        BaseTestCase.setUp(self)

        suite = unittest.TestSuite()

        user_tests = unittest.TestLoader().discover(start_dir='app/user/test', pattern='test_*.py')
        vendor_tests = unittest.TestLoader().discover(start_dir='app/vendor/test', pattern='test_*.py')
        product_tests = unittest.TestLoader().discover(start_dir='app/product/test', pattern='test_*.py')
        contact_tests = unittest.TestLoader().discover(start_dir='app/contact/test', pattern='test_*.py')
        notes_tests = unittest.TestLoader().discover(start_dir='app/notes/test', pattern='test_*.py')
        attachment_tests = unittest.TestLoader().discover(start_dir='app/attachment/test', pattern='test_*.py')

        suite.addTests(user_tests)
        suite.addTests(vendor_tests)
        suite.addTests(product_tests)
        suite.addTests(contact_tests)
        suite.addTests(notes_tests)
        suite.addTests(attachment_tests)    

        return suite

if __name__ == '__main__':
    # Set the environment to test
    environment = 'test'
    logging.info('Environment: {}'.format(environment)) 

    app = create_app(environment)
    with app.app_context():
        result = unittest.TextTestRunner(verbosity=2).run(TestApp().suite())    
        exit(not result.wasSuccessful())