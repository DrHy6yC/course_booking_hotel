from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as router_auth
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.init import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router_auth)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_hotels)
app.include_router(router_rooms)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        reload=True
    )
