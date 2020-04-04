import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:

    SECRET_KEY = os.getenv('SECRET_KEY') or 'not set'
    CURRENT_VERSION = os.getenv('CURRENT_VERSION') or 'not set'
    SERVICE_NAME = os.getenv('SERVICE_NAME') or 'not set'
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLITE database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class TestingConfig(Config):
    DEBUG = True
    # SQLITE database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app-test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False    
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    DEBUG = False
    # Postgres
    # DB_USER = os.getenv('DB_USER') or 'not set'
    # DB_PASSWORD = os.getenv('DB_PASSWORD') or 'not set'
    # DB_HOST = os.getenv('DB_HOST') or 'not set'
    # DB_PORT = os.getenv('DB_PORT') or 'not set'
    # DB_NAME = os.getenv('DB_NAME') or 'not set'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USER,
    #                                                                DB_PASSWORD,
    #                                                                DB_HOST,
    #                                                                DB_PORT,
    #                                                                DB_NAME)


config_by_name = dict(
    development=DevelopmentConfig,
    test=TestingConfig,
    production=ProductionConfig
)    