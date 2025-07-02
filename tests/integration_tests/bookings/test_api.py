from datetime import date, timedelta
import pytest


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
    if response.status_code == 422:
        error_message = response.json().get("detail", "")
        print(f"Error message: {error_message}")
        assert "specific error message" in error_message
    assert response.status_code == status_code
    if status_code == 200:
        data = response.json()
        assert isinstance(data, dict)
        assert room_id == data["booking"]["room_id"]
        assert data["status"] == "OK"
