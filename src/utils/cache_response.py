import json
import functools
from typing import Callable, Any
from fastapi import Request

from src.utils.redis_manager import RedisManager


def cache_response(redis: RedisManager, expire: int = 60):

    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")

            if not request:
                raise ValueError("Request object is required in endpoint for caching")

            path = request.url.path
            query = str(sorted(request.query_params.items()))
            cache_key = f"cache:{path}:{query}"

            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)

            response = await func(*args, **kwargs)

            await redis.set(cache_key, json.dumps(response), expire=expire)

            return response

        return wrapper

    return decorator
