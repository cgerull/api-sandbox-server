"""Default flask application configuration"""
import os

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Only_the_default_secret_key'
    SECRET_FILE = '/run/secrets/my_secret_key'
    CONFIG_FILE = './srv-config.yml'
    ACCESS_LOG = os.environ.get('ACCESS_LOG') or './access.log'
    ERROR_LOG = os.environ.get('ERROR_LOG') or './error.log'
    LOG_LINES = 30
    REDIS_SERVER = os.environ.get('REDIS_SERVER') or ''
    REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
    REDIS_HTML_COUNTER = "api_srv_html_counter"
    REDIS_API_COUNTER = "api_srv_counter"
