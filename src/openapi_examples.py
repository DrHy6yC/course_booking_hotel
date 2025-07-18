from datetime import date, timedelta

from fastapi.openapi.models import Example

admin_example = Example(
    summary="Админ",
    value={
        "login": "di",
        "name": "admin",
        "email": "admin@h.ru",
        "age": 12,
        "password": "111",
    },
)

user_example = Example(
    summary="Пользователь",
    value={
        "login": "Zurab",
        "name": "Ashot",
        "email": "za@h.ru",
        "age": 12,
        "password": "000",
    },
)

admin_login_example = Example(
    summary="Админ",
    value={
        "email": "admin@h.ru",
        "password": "111",
    },
)

hotel_sochi = Example(
    summary="Сочи",
    value={
        "title": "Отель Сочи 5 звезд у моря",
        "location": "Сочи, ул Моря, д, 12",
    },
)

hotel_dubai = Example(
    summary="Дубай",
    value={
        "title": "Отель Дубай У фонтана",
        "location": "Дубай, ул Фонтана, д, 12",
    },
)

room_standard = Example(
    summary="Стандарт",
    value={
        "title": "Номер стандарт",
        "description": "",
        "price": 2500,
        "quantity": 4,
        "facilities_ids": [],
    },
)

date_today = Example(summary="Cегодня", value=date.today())
date_tomorrow = Example(
    summary="Завтра", value=date.today() + timedelta(days=1)
)
