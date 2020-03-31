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
    redis_connection = None
    if app.config["REDIS_URL"]:
        try:
            print("Connect to Redis at {}".format(app.config["REDIS_URL"]))
            redis_connection = redis.from_url(app.config["REDIS_URL"])
        except Exception as exc:
            print("Error connecting to Redis: {}".format(exc))
    return redis_connection

def increment_redis_counter(redis_connection, counter='counter'):
    """
    Increase a counter variable in Redis.

    Args:
        redis_connection: A Redis connection
        counter: The name of the variable to be increased, defaults to counter.
    """
    if redis_connection.get(counter):
        cnt = int(redis_connection.get(counter)) + 1
        redis_connection.set(counter, cnt)
    else:
        redis_connection.set(counter, "1")
