import json

import pytest
from httpx import ASGITransport, AsyncClient

from src.config import settings
from src.connectors.database_init import (
    BaseORM,
    async_session_maker_null_pool,
    engine_null_pool,
)
from src.main import app
from src.models import *
from src.schemas.hotel import HotelAdd
from src.schemas.facility import FacilityAdd
from src.schemas.room import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def async_setup_db(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
        await conn.run_sync(BaseORM.metadata.create_all)


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async with DBManager(session_factories=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test.ru"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def async_fill_db(async_setup_db):
    with open(file="tests/mock_hotels.json", mode="r", encoding="utf-8") as f_h:
        hotel_data = json.load(f_h)

    with open(file="tests/mock_facilities.json", mode="r", encoding="utf-8") as f_f:
        facilities_data = json.load(f_f)

    with open(file="tests/mock_rooms.json", mode="r", encoding="utf-8") as f_r:
        room_data = json.load(f_r)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotel_data]
    facilities = [FacilityAdd.model_validate(facility) for facility in facilities_data]
    rooms = [RoomAdd.model_validate(room) for room in room_data]
    async with DBManager(session_factories=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.facilities.add_bulk(facilities)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session", autouse=True)
async def create_user(ac, async_fill_db):
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
