from fastapi import APIRouter, Body, HTTPException, Query, status


from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotel import HotelAdd, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    path="",
    summary="Получение списка отелей",
    description="Можно получить список по локации или по названию отеля",
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
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=limit,
            offset=offset
        )


@router.get(
    path="/{hotels_id}",
    summary="Получение информации по одному отелю",
    description="Можно получить один отель по айди"
)
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post(
    path="",
    summary="Добавление нового отеля",
    description="Необходимо ввести title и name, id генерируется автоматически",
)
async def create_hotel(
        hotel_data: HotelAdd = Body(
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
            }
        )
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "hotel": result}


@router.put(
    path="/{hotel_id}",
    summary="Изменение уже существующего отеля по id",
    description="Необходимо ввести все параметры",
)
async def all_hotel_changes(
        hotel_id: int,
        hotel_data: HotelAdd,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(id=hotel_id,model_data=hotel_data)
        await session.commit()
    return {"status": "OK"}


@router.patch(
    path="/{hotel_id}",
    summary="Изменение уже существующего отеля по id",
    description="Можно изменить любой из параметров, а так же все параметры",
)
async def hotel_changes(
        hotel_id: int,
        hotel_data: HotelPatch
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(id=hotel_id, model_data=hotel_data, exclude_unset=True)
        await session.commit()
    return {"status": "OK"}


@router.delete(
    path="/{hotel_id}",
    summary="Удаление уже существующего отеля по id",
    description="Удаляем отель по id",
)
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).delete(id=hotel_id)
        if result == 200:
            await session.commit()
            return {"status": "OK"}
        elif result == 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"status": "Error - NOT_FOUND"})
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"status": "Error - BAD_REQUEST"})


