from flask_redis import FlaskRedis
from redis import Redis

redis_client: Redis = FlaskRedis(charset="utf-8", decode_responses=True)
