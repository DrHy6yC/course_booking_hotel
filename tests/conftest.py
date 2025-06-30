import json

import pytest
from httpx import ASGITransport, AsyncClient

from src.config import settings
from src.connectors.database_init import BaseORM, engine_null_pool
from src.main import app
from src.models import *


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def async_setup_db(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
        await conn.run_sync(BaseORM.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def async_fill_db(async_setup_db):
    with open(file="tests/mock_hotels.json", mode="r", encoding="utf-8") as f_h:
        data = json.load(f_h)
        for hotel in data:
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test.ru"
            ) as ac:
                result_hotel = await ac.post(url="/hotels", json=hotel)
                assert result_hotel.status_code == 200
                assert result_hotel

    with open(file="tests/mock_facilities.json", mode="r", encoding="utf-8") as f_h:
        data = json.load(f_h)
        for facility in data:
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test.ru"
            ) as ac:
                result_facility = await ac.post(url="/facilities", json=facility)
                assert result_facility.status_code == 200
                assert result_facility

    with open(file="tests/mock_rooms.json", mode="r", encoding="utf-8") as f_h:
        data = json.load(f_h)
        for room in data:
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test.ru"
            ) as ac:
                result_room = await ac.post(
                    url=f"/hotels/{room['hotel_id']}/rooms", json=room
                )
                assert result_room.status_code == 200
                assert result_room


@pytest.fixture(scope="session", autouse=True)
async def create_user(async_fill_db):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test.ru"
    ) as ac:
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
