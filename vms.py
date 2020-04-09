import os
import unittest
from dotenv import load_dotenv
from app import create_app


environment = os.environ.get('FLASK_ENV') or 'development'

app = create_app(environment)
print("Environment: {}".format(environment))


@app.cli.command()
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1
