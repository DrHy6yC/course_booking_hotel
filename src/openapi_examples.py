from fastapi.openapi.models import Example

admin_example= Example(
    summary="Админ",
    value={
        "login":"di",
        "name": "admin",
        "email": "admin@h.ru",
        "age": "12",
        "password": "111",
    }
)

user_example = Example(
    summary="Пользователь",
    value={
        "login":"Zurab",
        "name": "Ashot",
        "email": "za@h.ru",
        "age": "12",
        "password": "000",
    }
)

admin_login_example = Example(
    summary="Админ",
    value={
        "email": "admin@h.ru",
        "password": "111",
    }
)