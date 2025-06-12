from fastapi import APIRouter, Body, Query
from pydantic import BaseModel


router = APIRouter(prefix="/hotels", tags=["Отели"])


class Hotel(BaseModel):
    title: str
    name: str


hotels = [
    {"id": 1, "title": "Sochi", "name": "Sochi Luxe"},
    {"id": 2, "title": "Дубай", "name": "Luxury Dubai Hotel"},
]


@router.get(
    path="",
    summary="Получение списка отелей",
    description="Можно получить список по айдишнику или по названию отеля",
)
def get_hotels(
        id: int | None = Query(default=None, description="Айдишник"),
        title: str | None = Query(default=None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@router.post(
    path="",
    summary="Добавление нового отеля",
    description="Необходимо ввести title и name, id генерируется автоматически",
)
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": Hotel.title,
        "name": Hotel.name,
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
            hotel["title"] = Hotel.title
            hotel["name"] = Hotel.name
    return {"status": "OK"}


@router.patch(
    path="/{hotel_id}",
    summary="Изменение уже существующего отеля по id",
    description="Можно изменить любой из параметров, а так же все параметры",
)
def hotel_changes(
        hotel_id: int,
        title: str | None = Body(default=None, embed=True),
        name: str | None = Body(default=None, embed=True),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
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