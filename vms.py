import os
import unittest
from flask_cors import CORS
from dotenv import load_dotenv
from app import create_app
from vms_test_suite import TestApp


environment = os.environ.get('FLASK_ENV') or 'development'

app = create_app(environment)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
print("Environment: {}".format(environment))


# @app.before_request
# def before_request_func():
#     # print("before_request is running!")
#     # add code here to inspect headers


@app.cli.command()
def test():
    """Runs the unit tests."""
    result = unittest.TextTestRunner(verbosity=2).run(TestApp().suite())
    if result.wasSuccessful():
        return 0
    return 1
