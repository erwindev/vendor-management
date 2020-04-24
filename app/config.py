import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:

    SECRET_KEY = os.getenv('SECRET_KEY') or 'notsosecretkey'
    CURRENT_VERSION = os.getenv('CURRENT_VERSION') or 'development'
    SERVICE_NAME = os.getenv('SERVICE_NAME') or 'Vendor Management System'
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLITE database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_POOL_SIZE = None


class TestingConfig(Config):
    DEBUG = True
    # SQLITE database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app-test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False    
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_POOL_SIZE = None


class ProductionConfig(Config):
    DEBUG = False
    # Postgres
    POSTGRES_USER = os.getenv('POSTGRES_USER') or 'not set'
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD') or 'not set'
    POSTGRES_HOST = os.getenv('POSTGRES_HOST') or 'not set'
    POSTGRES_PORT = os.getenv('POSTGRES_PORT') or 'not set'
    POSTGRES_DB = os.getenv('POSTGRES_DB') or 'not set'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(POSTGRES_USER,
                                                                   POSTGRES_PASSWORD,
                                                                   POSTGRES_HOST,
                                                                   POSTGRES_PORT,
                                                                   POSTGRES_DB)
    SQLALCHEMY_POOL_SIZE = os.getenv('SQLALCHEMY_POOL_SIZE') or 10
    SQLALCHEMY_TRACK_MODIFICATIONS = False                                                                   


config_by_name = dict(
    development=DevelopmentConfig,
    test=TestingConfig,
    production=ProductionConfig
)    