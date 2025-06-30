async def test_get_facilities(ac):
    response = await ac.get(url="/facilities")
    assert response.status_code == 200


async def test_post_facilities(ac):
    response = await ac.post(
        url="/facilities",
        json={"title": "Бесплатный Wi-Fi"},
    )
    assert response.status_code == 200
