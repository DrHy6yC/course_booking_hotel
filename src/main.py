import sys

from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.api.auth import router as router_auth
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.tasks import router as router_tasks
from src.connectors.redis_init import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(
        RedisBackend(redis_manager._redis), prefix="fastapi-cache"
    )
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router_auth)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_tasks)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
