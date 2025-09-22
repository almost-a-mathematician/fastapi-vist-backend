from redis.asyncio import StrictRedis
import os

cache_manager = StrictRedis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    db=os.getenv('REDIS_DB'),
    password=os.getenv('REDIS_PASSWORD'),
    decode_responses=True
)