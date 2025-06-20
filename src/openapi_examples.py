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

hotel_sochi = Example(
    summary="Сочи",
    value= {
        "title": "Отель Сочи 5 звезд у моря",
        "location": "Сочи, ул Моря, д, 12",
    }
)

hotel_dubai = Example(
    summary="Дубай",
    value={
        "title": "Отель Дубай У фонтана",
        "location": "Дубай, ул Фонтана, д, 12",
    }
)

room_standart = Example(
    summary="Стандарт",
    value={
        "hotel_id": "5",
        "title": "Номер стандарт",
        "description": "" ,
        "price": "2500",
        "quantity": "4",
    }
)