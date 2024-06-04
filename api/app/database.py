import redis

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0
PEERS_KEY = 'peers'


def get_redis_client():
    return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
