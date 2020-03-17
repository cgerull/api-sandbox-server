"""Default flask application configuration"""
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    APP_NAME = 'Echo Webserver'
    APP_FOOTER = 'Default configuration'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Only_the_default_secret_key'
    SECRET_FILE = '/run/secrets/my_secret_key'
    # CONFIG_FILE = './srv-config.yml'
    ACCESS_LOG = os.environ.get('ACCESS_LOG') or None
    ERROR_LOG = os.environ.get('ERROR_LOG') or None
    LOG_LINES = 30
    # Redis
    REDIS_URL = os.environ.get("REDIS_URL") or None
    REDIS_SERVER = os.environ.get('REDIS_SERVER') or None
    REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
    REDIS_HTML_COUNTER = 'api_srv_html_counter'
    REDIS_API_COUNTER = 'api_srv_counter'
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
