#!/usr/bin/env python3
"""
Defines a Cache class
"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator Function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper Function"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """Represents a cache"""
    def __init__(self):
        """Initialize the class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generates a random key

        Keyword arguments:
        data -- Input data to store in Redis
        Return: Key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[
            str, bytes, int, float, None]:
        """Gets and convert the data back to the desired format
        """
        data = self._redis.get(key)
        if fn and data:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """Gets and convert the data a string data"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """Gets and convert the data an int data"""
        return self.get(key, fn=int)
