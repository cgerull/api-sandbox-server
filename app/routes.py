"""
Route module for timeconverter web api
"""
from app import app
from flask import (request, jsonify, render_template, redirect,
                   url_for, flash, make_response)

from datetime import datetime
import socket
import os
import yaml

from app.redis_tools import get_redis
from app.redis_tools import increment_redis_counter

# Modules constants
secret_file = '/run/secrets/my_secret_key'
config_file = '/srv-config'
srv_config = {
    'title': 'Echo Webserver',
    'footer': 'Default configuration'
}
localhost = socket.gethostname()
my_redis = get_redis()


#
# HTML endpoints
##############################################################################
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    Respond as echo with:
        timestamp,
        local_ip,
        container_name / hostname,
        secret,
        remote_ip: requester ip or proxy ip,
        client_ip

    If a Redis server is defined, keeps a dynamic count of pageviews 
    for HTML and API echo requests.
    """
    # read_config(srv_config)
    page_view = 0
    response_data = build_response_data()
    if my_redis:
        increment_redis_counter(my_redis, app.config['REDIS_HTML_COUNTER'])
        page_view = int(my_redis.get(app.config['REDIS_HTML_COUNTER']))
    
    resp = make_response(render_template('index.html',
                        title=app.config['APP_NAME'],
                        footer=app.config['APP_FOOTER'],
                        resp=response_data,
                        page_view=page_view))
    resp.headers['Server-IP'] = socket.gethostbyname(localhost)
    return resp


#
# Logs page
@app.route('/logs', methods=['GET'])
def logs():
    """
    If log files are written locally,
    tail log data.
    """
    # read_config(config_file, srv_config)
    a_log = tail_logfile(app.config['ACCESS_LOG'])
    resp = make_response(render_template('logs.html',
                        title=app.config['APP_NAME'],
                        footer=app.config['APP_FOOTER'],
                        a_log=a_log))
    resp.headers['Server-IP'] = socket.gethostbyname(localhost)
    return resp


def mongodb():
    """
    Simple form to get and set a note in MongoDB
    """
    pass


def postgresql():
    """
    Simple form to get and set a note in PostgreSql.
    """
    pass


#
# REST API
##############################################################################
@app.route('/api/echo', methods=['GET'])
def api_echo():
    """
    API endpoint for echo data.

    Returns:
        See index
    """
    resp = make_response(jsonify(build_response_data()))
    resp.headers['Server-IP'] = socket.gethostbyname(localhost)
    return resp


@app.route('/api/config', methods=['GET'])
def api_config():
    """
    API endpoint for config data.

    Returns:
        The complete app.config object.
        DON'T USE THIS IN A REAL APPLICATION!
    """
    # read_config(srv_config)
    resp = make_response(jsonify_config())
    resp.headers['Server-IP'] = socket.gethostbyname(localhost)
    return resp


#
# Utiliy functions
# ############################################################################
def build_response_data():
    """
    Build a dictionary with timestamp, server ip,
    server name, secret and requester ip.
    """
    localhost = socket.gethostname()
    return {
        'now': datetime.now().isoformat(sep=' '),
        'local_ip': socket.gethostbyname(localhost),
        'container_name': localhost,
        'secret': get_secret_key(),
        'remote_ip': request.remote_addr,
        'client_ip': request.access_route[0]
    }


def get_secret_key():
    """
    Return secret key from:
        Docker secret file or
        Environment variable SECRET_KEY or
        a default value
    
    Returns:
        the secret string
    """
    secret = ''
    try:
        f = open(secret_file, 'r')
        secret = f.read()
    except:
        # no file, just return empty string
        # secret = os.environ.get('SECRET_KEY') or 'Only_the_default_secret_key'
        secret = app.config['SECRET_KEY']
    return secret


def jsonify_config():
    """
    Return:
        A JSON representation of the current configuration data.
    """
    a_config = {}
    for key in app.config:
        a_config[key] = str(app.config[key])
        # print("app.config[{}]: {}".format(key, a_config[key]))
    return jsonify(a_config)


def tail_logfile(logfile = None):
    """
    Read n lines of a logfile.

    Args:
        logfile: Name of the logfile, default is None

    Returns:
        The truncated logfile.
    """
    result = "No logfiles available"
    lines = app.config['LOG_LINES']
    if logfile: 
        try:
            with open(logfile) as f:
                result = ''.join(f.readlines()[-lines:])
        except Exception as exc:
            print("Can't open logfile. {}".format(exc))
    return result
