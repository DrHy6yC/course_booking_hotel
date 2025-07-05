# ruff: noqa: E402
import json

from typing import AsyncGenerator
from unittest import mock

mock.patch(
    "fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f
).start()


import pytest

from httpx import ASGITransport, AsyncClient
from src.api.dependencies import get_db
from src.config import settings
from src.connectors.database_init import (
    BaseORM,
    async_session_maker_null_pool,
    engine_null_pool,
)
from src.main import app
from src.models import *  # noqa: F403
from src.schemas.facility import FacilityAdd
from src.schemas.hotel import HotelAdd
from src.schemas.room import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode() -> None:
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def async_setup_db(check_test_mode) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
        await conn.run_sync(BaseORM.metadata.create_all)


async def get_db_null_pool() -> AsyncGenerator[DBManager, None]:
    async with DBManager(
        session_factories=async_session_maker_null_pool
    ) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test.ru"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def async_fill_db(async_setup_db) -> None:
    with open(file="tests/mock_hotels.json", encoding="utf-8") as f_h:
        hotel_data = json.load(f_h)

    with open(file="tests/mock_facilities.json", encoding="utf-8") as f_f:
        facilities_data = json.load(f_f)

    with open(file="tests/mock_rooms.json", encoding="utf-8") as f_r:
        room_data = json.load(f_r)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotel_data]
    facilities = [
        FacilityAdd.model_validate(facility) for facility in facilities_data
    ]
    rooms = [RoomAdd.model_validate(room) for room in room_data]
    async with DBManager(
        session_factories=async_session_maker_null_pool
    ) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.facilities.add_bulk(facilities)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session", autouse=True)
async def create_user(ac, async_fill_db) -> None:
    (
        await ac.post(
            url="/auth/register",
            json={
                "login": "di",
                "name": "admin",
                "email": "admin@h.ru",
                "age": "12",
                "password": "111",
            },
        )
    )


@pytest.fixture(scope="session")
async def ac_with_token(ac, create_user) -> AsyncGenerator[AsyncClient, None]:
    await ac.post(
        url="/auth/login",
        json={
            "email": "admin@h.ru",
            "password": "111",
        },
    )
    assert ac.cookies["access_token"]
    yield ac
