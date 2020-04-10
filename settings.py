import os


RMSP_FETCH_TTL = 5 * 60

REDIS_TYPE = os.getenv('REDIS_TYPE')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_URL = os.getenv('REDIS_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}/0')
