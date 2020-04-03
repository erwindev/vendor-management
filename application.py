import os
from app import create_app

environment = os.environ.get('FLASK_ENVx') or 'development'

app = create_app(environment)

