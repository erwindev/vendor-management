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
