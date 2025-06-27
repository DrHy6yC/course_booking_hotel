import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import uvicorn

import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))

from src.api.dependencies import get_db
from src.connectors.redis_init import redis_manager

from src.api.auth import router as router_auth
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.tasks import router as router_tasks


async def get_bookings_with_today_checkin_helper():
    async for db in get_db():
        bookings_get = await db.bookings.get_bookings_with_today_checkin()
        print(f"\n{bookings_get}\n")

async def run_send_email_regularly():
    while True:
        await get_bookings_with_today_checkin_helper()
        await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(run_send_email_regularly())
    await redis_manager.connect()
    FastAPICache.init(
        RedisBackend(redis_manager.redis),
        prefix="fastapi-cache"
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
    uvicorn.run(
        app="main:app",
        reload=True
    )
