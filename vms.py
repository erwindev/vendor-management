import os
import unittest
from flask_cors import CORS
from app import app
from vms_test_suite import TestApp

    
cors = CORS(app, resources={r"/*": {"origins": "*"}})    


@app.cli.command()
def test():
    """Runs the unit tests."""
    result = unittest.TextTestRunner(verbosity=2).run(TestApp().suite())
    if result.wasSuccessful():
        return 0
    return 1

@app.cli.command()
def coverage():
    """Run test coverage using the existing test suite."""
    
    # Run the test suite with coverage
    os.system('coverage run vms_test_suite.py')
    
    # Generate terminal report
    os.system('coverage report --omit="app/*/test/*.py" app/*/*/*.py')
    
    # Generate HTML report
    os.system('coverage html --omit="app/*/test/*.py" app/*/*/*.py')
    

@app.before_request
def before_request_func():
    pass


if __name__ == "__main__":
    app.run()    
