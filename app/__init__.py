from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)

    bootstrap.init_app(app)

    # load the config
    app.config.from_object(config_class)

    # initialize the database and create tables
    from app.vendor import models
    db.init_app(app)
    migrate.init_app(app, db)

    # import blueprints
    from app.vendor.controller import vendor_app
    from app.vendor.api import apiv1

    # register the blueprints
    app.register_blueprint(vendor_app)
    app.register_blueprint(apiv1)

    login.init_app(app)
    login.login_view = 'vendor_app.login'

    return app
