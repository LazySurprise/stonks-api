"""Flask config."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    REDDIT_SECRET = environ.get('REDDIT_SECRET')
    REDDIT_ID = environ.get('REDDIT_ID')
    #SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    #STATIC_FOLDER = 'static'
    #TEMPLATES_FOLDER = 'templates'


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    #DATABASE_URI = environ.get('DEV_DATABASE_URI')
