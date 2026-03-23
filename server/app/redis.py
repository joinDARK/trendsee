from functools import lru_cache

import redis.asyncio as redis

from app.config import SETTINGS


@lru_cache()
def get_redis_client():
    return redis.Redis(host=SETTINGS.REDIS_HOST, port=6379, db=0, decode_responses=True)
