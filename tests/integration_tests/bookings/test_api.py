async def test_post_booking(db, ac_with_token):
    room_id = 1
    response = await ac_with_token.post(
        url="/bookings",
        json={"room_id": room_id, "date_from": "2025-06-30", "date_to": "2025-06-30"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert room_id == data["booking"]["room_id"]
    assert data["status"] == "OK"
