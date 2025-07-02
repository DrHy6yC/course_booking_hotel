import pytest


@pytest.mark.parametrize(
    "login, name, email, age, password, status_code,",
    [
        ("Zurab", "Ashot", "za@h.ru", 12, "000", 200),
        ("di", "admin", "admin@h.ru", 34, "111", 409),
    ],
)
async def test_login_logout(login, name, email, age, password, status_code, db, ac):
    result_register = await ac.post(
        url="auth/register",
        json={
            "login": login,
            "name": name,
            "email": email,
            "age": age,
            "password": password,
        },
    )
    assert result_register.status_code == status_code

    if result_register.status_code == 200:

        result_login = await ac.post(
            url="auth/login",
            json={
                "email": email,
                "password": password,
            },
        )
        assert result_login.status_code == 200
        assert isinstance(result_login.json(), str)

        result_me = await ac.get(url="auth/me")
        assert result_me.status_code == 200
        data_me = result_me.json()
        assert data_me["login"] == login
        assert data_me["name"] == name
        assert data_me["email"] == email
        assert data_me["age"] == age

        result_logout = await ac.post(url="auth/logout")
        assert result_logout.status_code == 200

        result_me_retry = await ac.get(url="auth/me")
        assert result_me_retry.status_code == 401
        data_me_retry = result_me_retry.json()
        assert (
            data_me_retry["detail"]["status"]
            == "Error - нет активного пользователя, залогиньтесь"
        )
