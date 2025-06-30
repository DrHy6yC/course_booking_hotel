async def test_get_facilities(ac):
    response = await ac.get(url="/facilities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_post_facilities(ac):
    facility_title = "Бесплатный Wi-Fi"
    response = await ac.post(
        url="/facilities",
        json={"title": facility_title},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert facility_title == data["facility"]["title"]
    assert data["status"] == "OK"
