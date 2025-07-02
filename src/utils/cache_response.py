import json
import functools
from typing import Callable, Any
from fastapi import Request

from src.utils.redis_manager import RedisManager


def cache_response(redis: RedisManager, expire: int = 60) -> Callable:
    """
    Декоратор для кэширования ответов эндпоинтов.

    :param redis: Экземпляр RedisManager для работы с Redis.
    :param expire: Время жизни кэша в секундах (по умолчанию 60 секунд).
    :return: Декорированная функция.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            request: Request = kwargs.get("request")

            if not request:
                raise ValueError("Request object is required in endpoint for caching")

            # Создаем ключ для кэша на основе пути и параметров запроса
            path: str = request.url.path
            query: str = str(sorted(request.query_params.items()))
            cache_key: str = f"cache:{path}:{query}"

            # Проверяем, есть ли кэшированный ответ
            cached: str | None = await redis.get(cache_key)
            if cached:
                return json.loads(cached)

            # Вызываем оригинальную функцию и сохраняем результат в кэш
            response: Any = await func(*args, **kwargs)

            # Сериализуем ответ в JSON и сохраняем в Redis
            await redis.set(cache_key, json.dumps(response), expire=expire)

            return response

        return wrapper

    return decorator
