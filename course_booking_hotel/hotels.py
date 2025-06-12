from fastapi import APIRouter, Body, Query

from schemas.hotel import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get(
    path="",
    summary="Получение списка отелей",
    description="Можно получить список по айдишнику или по названию отеля",
)
def get_hotels(
        id: int | None = Query(default=None, description="Айдишник"),
        title: str | None = Query(default=None, description="Название отеля"),
        page: int | None = Query(default=1, description="Номер страницы", gt=1),
        per_page: int | None = Query(default=3, description="Количество отелей на странице", gt=1, lt=10),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    start_cut = per_page * (page - 1)
    end_cut = per_page * page
    return hotels_[start_cut:end_cut]


@router.post(
    path="",
    summary="Добавление нового отеля",
    description="Необходимо ввести title и name, id генерируется автоматически",
)
def create_hotel(hotel_data: Hotel = Body(
    openapi_examples={
        "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "name": "sochi_u_morya",
                }
            },
        "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай У фонтана",
                    "name": "dubai_fountain",
                }
            },
    })
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "OK"}


@router.put(
    path="/{hotel_id}",
    summary="Изменение уже существующего отеля по id",
    description="Необходимо ввести все параметры",
)
def all_hotel_changes(
        hotel_id: int,
        hotel_data: Hotel,
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch(
    path="/{hotel_id}",
    summary="Изменение уже существующего отеля по id",
    description="Можно изменить любой из параметров, а так же все параметры",
)
def hotel_changes(
        hotel_id: int,
        hotel_data: HotelPatch
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.delete(
    path="/{hotel_id}",
    summary="Удаление уже существующего отеля по id",
    description="Удаляем отель по id",
)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
