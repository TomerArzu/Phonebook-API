import redis

from domain.repositories import RequestResponseCachedRepository


import json


class RedisRequestResponseCachedRepository(RequestResponseCachedRepository):

    def __init__(self, redis_client):
        self._redis_client: redis.Redis = redis_client
        self._cache_valid = False

    def set_cache_request(self, request_key, response):
        self._redis_client.set(request_key, json.dumps(response))

    def get_cached_response(self, request_key):
        cached_response = None
        if self._cache_valid:
            try:
                cached_response = tuple(json.loads(self._redis_client.get(request_key)))
            except TypeError:
                pass
        return cached_response

    def invalidate_cache(self) -> None:
        self._cache_valid = False
        self._delete_cached_requests()

    def set_cache_valid(self):
        self._cache_valid = True

    def _delete_cached_requests(self):
        keys_to_delete = self._redis_client.keys('CachedRequest:*')
        if keys_to_delete:
            self._redis_client.delete(*keys_to_delete)
