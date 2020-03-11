"""
Redis functions.

Redis connection and utility functions.
"""
import redis

from app import app

def get_redis():
    """
    Return a connection to a Redis server if defined.
    """
    r = None
    if app.config["REDIS_URL"]:
        print("Connect to Redis at {}".format(app.config["REDIS_URL"]))
        r = redis.from_url(app.config["REDIS_URL"])
    return r

def increment_redis_counter(r, counter = 'counter'):
    """
    Increase a counter variable in Redis.

    Args:
        r: A Redis connection
        counter: The name of the variable to be increased, defaults to counter.
    """
    c =+ r.get(counter)
    r.set(counter, c)
