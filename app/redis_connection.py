import redis
from app import app

def get_redis():
    r = None
    if app.config["REDIS_URL"]:
        print("Connect to Redis at {}".format(app.config["REDIS_URL"]))
        r = redis.from_url(app.config["REDIS_URL"])
    return r

def increment_redis_counter(r, counter = 'counter'):
    c =+ r.get(counter)
    r.set(counter, c)
