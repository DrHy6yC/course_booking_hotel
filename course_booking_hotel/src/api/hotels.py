from fastapi import APIRouter, Body, Query
from sqlalchemy import insert, select


from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsORM
from src.schemas.hotel import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    path="",
    summary="Получение списка отелей",
    description="Можно получить список по айдишнику или по названию отеля",
)
async def get_hotels(
        paginations: PaginationDep,
        title: str | None = Query(default=None, description="Название отеля"),
        location: str | None = Query(default=None, description="Адрес отеля"),
):
    per_page = paginations.per_page or 5
    limit = per_page
    offset = per_page * (paginations.page - 1)
    async with async_session_maker() as session:
        query = select(HotelsORM)
        if title:
            query = query.filter_by(title=title)
        if location:
            query = query.filter_by(location=location)
        query = (
            query.
            limit(limit).
            offset(offset)
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
    return hotels


@router.post(
    path="",
    summary="Добавление нового отеля",
    description="Необходимо ввести title и name, id генерируется автоматически",
)
async def create_hotel(hotel_data: Hotel = Body(
    openapi_examples={
        "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "location": "Сочи, ул Моря, д, 12",
                }
            },
        "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай У фонтана",
                    "location": "Дубай, ул Фонтана, д, 12",
                }
            },
    })
):
    async  with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()
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
