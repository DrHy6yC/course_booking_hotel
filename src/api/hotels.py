from datetime import date

from fastapi import APIRouter, Body, HTTPException, Query, status
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.openapi_examples import date_today, date_tomorrow, hotel_dubai, hotel_sochi
from src.schemas.hotel import HotelAdd, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    path="",
    summary="Получение списка всех существующих отелей",
    description="Можно получить список по локации или по названию отеля",
)
@cache(expire=10)
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Адрес отеля"),
):
    per_page = pagination.per_page or 5
    limit = per_page
    offset = per_page * (pagination.page - 1)
    return await db.hotels.get_all(
        title=title, location=location, limit=limit, offset=offset
    )


@router.get(
    path="/unoccupied",
    summary="Получение списка отелей",
    description="Получение списка отелей доступных для бронирования за период",
)
@cache(expire=10)
async def get_hotels_unoccupied(
    db: DBDep,
    pagination: PaginationDep,
    date_from: date = Query(openapi_examples={"1": date_today}),
    date_to: date = Query(openapi_examples={"1": date_tomorrow}),
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Адрес отеля"),
):
    per_page = pagination.per_page or 5
    limit = per_page
    offset = per_page * (pagination.page - 1)
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        title=title,
        location=location,
        limit=limit,
        offset=offset,
    )


@router.get(
    path="/{hotel_id}",
    summary="Получение информации по одному отелю",
    description="Можно получить один отель по айди",
)
@cache(expire=10)
async def get_hotel_by_id(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post(
    path="",
    summary="Добавление нового отеля",
    description="Необходимо ввести title и name, id генерируется автоматически",
)
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": hotel_sochi,
            "2": hotel_dubai,
        }
    ),
):
    result = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "hotel": result}


@router.put(
    path="/{hotel_id}",
    summary="Изменить отель по id",
    description="Изменить все параметры отеля по id",
)
async def put_hotel(
    hotel_id: int,
    hotel_data: HotelAdd,
    db: DBDep,
):
    await db.hotels.edit(id=hotel_id, model_data=hotel_data)
    await db.commit()
    return {"status": "OK"}


@router.patch(
    path="/{hotel_id}",
    summary="Изменить отель по id",
    description="Изменить некоторые параметры отеля по id",
)
async def edit_hotel(
    hotel_id: int,
    hotel_data: HotelPatch,
    db: DBDep,
):
    await db.hotels.edit(id=hotel_id, model_data=hotel_data, exclude_unset=True)
    await db.commit()
    return {"status": "OK"}


@router.delete(
    path="/{hotel_id}",
    summary="Удаление уже существующего отеля по id",
    description="Удаляем отель по id",
)
async def delete_hotel(
    hotel_id: int,
    db: DBDep,
):
    result = await db.hotels.delete(id=hotel_id)
    if result == 200:
        await db.commit()
        return {"status": "OK"}
    elif result == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "Error - NOT_FOUND"},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "Error - BAD_REQUEST"},
        )
