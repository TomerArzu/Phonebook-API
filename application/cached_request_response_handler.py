import hashlib
from utils.logger_instance import logger

from domain.repositories import RequestResponseCachedRepository


class CachedRequestResponseHandler:
    def __init__(self, request_response_cached_repository: RequestResponseCachedRepository):
        self._request_response_cached_repository = request_response_cached_repository

    def get_cached_response(self, request_method: str, request_url: str):
        cached_response = self._request_response_cached_repository.get_cached_response(
            self.create_request_key(request_method, request_url)
        )
        if cached_response:
            logger.debug("cache hit! response retrieved from cache")
        return cached_response

    def set_cache_request(self, request_method: str, request_url: str, response):
        request_key = self.create_request_key(request_method, request_url)
        self._request_response_cached_repository.set_cache_request(request_key, response)
        self._request_response_cached_repository.set_cache_valid()
        logger.debug("new request added to cache")

    def invalidate_cache(self):
        self._request_response_cached_repository.invalidate_cache()
        logger.debug("cache is no longer valid due to cached in database")

    @staticmethod
    def create_request_key(request_method: str, request_url: str):
        key_string = f"{request_method}:{request_url}"

        key_hash = "CachedRequest:" + hashlib.sha256(key_string.encode()).hexdigest()

        return key_hash
