import unittest
from app import create_app

class TestApp():
    def suite(self):
        suite = unittest.TestSuite()

        user_tests = unittest.TestLoader().discover(start_dir='app/user/test', pattern='test_*.py')
        # vendor_tests = unittest.TestLoader().discover(start_dir='app/vendor/test', pattern='test_*.py')
        # product_tests = unittest.TestLoader().discover(start_dir='app/product/test', pattern='test_*.py')
        # contact_tests = unittest.TestLoader().discover(start_dir='app/contact/test', pattern='test_*.py')
        # notes_tests = unittest.TestLoader().discover(start_dir='app/notes/test', pattern='test_*.py')
        # attachment_tests = unittest.TestLoader().discover(start_dir='app/attachment/test', pattern='test_*.py')

        suite.addTests(user_tests)
        # suite.addTests(vendor_tests)
        # suite.addTests(product_tests)
        # suite.addTests(contact_tests)
        # suite.addTests(notes_tests)
        # suite.addTests(attachment_tests)    

        return suite

if __name__ == '__main__':
    app = create_app()
    unittest.TextTestRunner(verbosity=2).run(TestApp().suite())    