import redis
from app import app

def get_redis():
    r = None
    if app.config["REDIS_URL"]:
        r = redis.from_url(os.environ.get("REDIS_URL"))
    return r

def increment_redis_counter(r, counter = 'counter'):
    c =+ r.get(counter)
    r.set(counter, c)
