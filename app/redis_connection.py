import redis
from app import app

def get_redis():
    r = None
    if app.config["REDIS_SERVER"]:
        r = redis.Redis(app.config["REDIS_SERVER"], app.config["REDIS_PORT"])
    return r

def increment_redis_counter(r, counter = 'counter'):
    c =+ r.get(counter)
    r.set(counter, c)
