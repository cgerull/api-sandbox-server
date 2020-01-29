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
from app.redis_connection import get_redis

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
# HTML page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """Build response data and send page to requester."""
    read_config(config_file, srv_config)
    page_view = 0
    response_data = build_response_data()
    if my_redis:
        increment_redis_counter(my_redis, app.config['REDIS_HTML_COUNTER'])
        page_view = int(my_redis.get(app.config['REDIS_HTML_COUNTER']))
    
    resp = make_response(render_template('index.html',
                        title=srv_config['title'],
                        footer=srv_config['footer'],
                        resp=response_data,
                        page_view=page_view))
    resp.headers['Server-IP'] = socket.gethostbyname(localhost)
    return resp


#
# Logs page
@app.route('/logs', methods=['GET'])
def logs():
    """Gather log data and send page to requester."""
    read_config(config_file, srv_config)
    a_log = tail_logfile(app.config['ACCESS_LOG'])
    resp = make_response(render_template('logs.html',
                        title=srv_config['title'],
                        footer=srv_config['footer'],
                        a_log=a_log))
    resp.headers['Server-IP'] = socket.gethostbyname(localhost)
    return resp


#
# REST API
@app.route('/api/echo', methods=['GET'])
def api_echo():
    """Build api endpoint for echo data."""
    resp = make_response(jsonify(build_response_data()))
    resp.headers['Server-IP'] = socket.gethostbyname(localhost)
    return resp


#
# REST API
@app.route('/api/config', methods=['GET'])
def api_config():
    """Build api endpoint for config data."""
    read_config(config_file, srv_config)
    resp = make_response(jsonify(srv_config))
    resp.headers['Server-IP'] = socket.gethostbyname(localhost)
    return resp

#
# Utiliy functions
# #################################################################################
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


def read_config(config_file, srv_config):
    """
    Read configuration from file and update srv_config dictionary.
    If no config file exists, a default configuration is used.
    Args:
        configuration file
        configuration dictonary
    """
    try:
        with open(config_file, 'r') as stream:
            config_data = (yaml.safe_load(stream))
            for key in config_data.keys():
                srv_config[key] = config_data[key]   
    except Exception as exc:
        print("Can't read configuration. {}".format(exc))


def tail_logfile(logfile=''):
    """Read n lines of the logfile"""
    result = "Can't read logfile: {}".format(logfile)
    lines = app.config['LOG_LINES']
    try:
        with open(logfile) as f:
            # for line in (f.readlines()[-lines:]):
            #     print(line)
            result = ''.join(f.readlines()[-lines:])
    except Exception as exc:
        print("Can't open logfile. {}".format(exc))
    return result


def increment_redis_counter(r, counter = 'counter'):
    if r.get(counter):
        c = int(r.get(counter)) + 1
        r.set(counter, c)
    else:
        r.set(counter, "1")
