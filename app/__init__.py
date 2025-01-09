import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from app.config import config_by_name
from app.appinfo import appinfo_bp
from flask_bcrypt import Bcrypt
import logging

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
bcrypt = Bcrypt()

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

def create_app():

    environment = os.environ.get('FLASK_ENV') or 'development'
    print('Environment: {}'.format(environment))

    app = Flask(__name__)

    bootstrap.init_app(app)

    # load the config
    app.config.from_object(config_by_name[environment])

    # initialize the database and create tables
    from app.user.models.user import User, BlackListToken
    from app.vendor.models.vendor import Vendor
    from app.product.models.product import Product  
    from app.contact.models.contact import Contact
    from app.notes.models.notes import Notes
    from app.attachment.models.attachment import Attachment
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # import blueprints
    from app.vendor.api import vendor_apiv1 
    from app.product.api import product_apiv1
    from app.contact.api import contact_apiv1    
    from app.attachment.api import attachment_apiv1
    from app.notes.api import notes_apiv1   
    from app.user.api import user_apiv1   

    # register the blueprints
    app.register_blueprint(vendor_apiv1)
    app.register_blueprint(product_apiv1)
    app.register_blueprint(contact_apiv1)
    app.register_blueprint(attachment_apiv1)
    app.register_blueprint(notes_apiv1)
    app.register_blueprint(user_apiv1)
    app.register_blueprint(appinfo_bp)

    # Add file handler
    if not app.debug:
        file_handler = logging.FileHandler('logs/vms.log')
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    return app

# Create the app instance
app = create_app()
