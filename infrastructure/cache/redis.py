import os

import redis

redis_client = redis.Redis(host="redis", port=6379, password="rise")
