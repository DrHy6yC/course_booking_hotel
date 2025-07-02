from datetime import date, timedelta
import pytest

from tests.conftest import get_db_null_pool


today = str(date.today())
tomorrow = str(date.today() + timedelta(days=1))
today_plus_2 = str(date.today() + timedelta(days=2))
today_plus_3 = str(date.today() + timedelta(days=3))


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (2, today, tomorrow, 200),
        (2, today, tomorrow, 200),
        (2, today, tomorrow, 404),
        (2, today_plus_2, today_plus_3, 200),
        (2, today, today_plus_3, 404),
    ],
)
async def test_post_booking(
    room_id, date_from, date_to, status_code, db, ac_with_token
):
    response = await ac_with_token.post(
        url="/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code
    if status_code == 200:
        data = response.json()
        assert isinstance(data, dict)
        assert room_id == data["booking"]["room_id"]
        assert data["status"] == "OK"


@pytest.fixture(scope="module")
async def delete_all_bookings_db():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, count_bookings",
    [
        (2, today, tomorrow, 1),
        (2, today, tomorrow, 2),
        (2, today, tomorrow, 2),
        (2, today_plus_2, today_plus_3, 3),
        (2, today, today_plus_3, 3),
    ],
)
async def test_add_and_get_bookings(
    room_id,
    date_from,
    date_to,
    count_bookings,
    db,
    ac_with_token,
    delete_all_bookings_db,
):
    await ac_with_token.post(
        url="/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    response = await ac_with_token.get(url="/bookings/me")
    assert response.status_code == 200
    data = response.json()
    if response.status_code == 200:
        assert len(data) == count_bookings


async def test_delete_booking(ac_with_token, db):
    response = await ac_with_token.delete(url="/bookings/me")
    assert response.status_code == 200
