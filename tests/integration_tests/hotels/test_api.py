async def test_get_hotels(ac):
    response = await ac.get(url="/hotels")
    assert response.status_code == 200
