from typing import Optional

import redis.asyncio as redis


class RedisManager:
    _redis: redis.Redis

    def __init__(self, redis_url: str) -> None:
        self.redis_url = redis_url

    async def connect(self) -> None:
        self._redis = await redis.from_url(
            url=self.redis_url,
        )

    async def set(
        self, key: str, value: str, expire: Optional[int] = None
    ) -> None:
        if expire is not None:
            await self._redis.set(key, value, ex=expire)
        else:
            await self._redis.set(key, value)

    async def get(self, key: str) -> Optional[str]:
        return await self._redis.get(key)

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)

    async def close(self):
        if self._redis:
            await self._redis.close()
