from src.services.auth import AuthServices


def test_create_access_token():
    data = {
        "user_id": "1",
    }
    jwt_token = AuthServices().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)
