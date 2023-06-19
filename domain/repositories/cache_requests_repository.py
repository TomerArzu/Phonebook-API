from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class RequestResponseCachedRepository(ABC):
    @abstractmethod
    def set_cache_request(self, request_key, response):
        """set new cache response with reques key"""
        ...

    @abstractmethod
    def get_cached_response(self, request_key):
        """get cached response by request"""
        ...

    @abstractmethod
    def invalidate_cache(self):
        """invalidate cache data and clear"""
        ...

    @abstractmethod
    def set_cache_valid(self):
        """ make cache valid for requests """
        ...
