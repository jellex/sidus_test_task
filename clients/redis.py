from aioredis import Redis

from config import config

redis_client = Redis.from_url(config.REDIS_URL, encoding="utf-8", decode_responses=True)
