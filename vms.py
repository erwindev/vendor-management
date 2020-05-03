import os
import unittest
from flask_cors import CORS
from app import create_app
from vms_test_suite import TestApp

    
app = create_app()
cors = CORS(app, resources={r"/*": {"origins": "*"}})    


@app.cli.command()
def test():
    """Runs the unit tests."""
    os.environ['FLASK_ENV'] = 'test'
    result = unittest.TextTestRunner(verbosity=2).run(TestApp().suite())
    if result.wasSuccessful():
        return 0
    return 1


@app.before_request
def before_request_func():
    pass


if __name__ == "__main__":
    app.run()    
