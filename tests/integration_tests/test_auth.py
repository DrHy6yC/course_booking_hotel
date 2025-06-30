from src.services.auth import AuthServices


def test_create_and_decode_access_token():
    data = {
        "user_id": "1",
    }
    jwt_token = AuthServices().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    pyload = AuthServices().decoded_access_token(jwt_token)

    assert pyload
    assert isinstance(pyload, dict)
    assert pyload["user_id"] == data["user_id"]
