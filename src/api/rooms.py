from fastapi import APIRouter, Body, HTTPException, Path, status

from src.database import async_session_maker
from src.openapi_examples import room_standart
from src.repositories.rooms import RoomsRepository
from src.schemas.room import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Номера"])


@router.get(
    path="",
    summary="Получение номеров",
    description="Получить все номера в отеле",
)
async def get_rooms(
        hotel_id: int = Path(description="Айди отеля"),
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filter_by(hotel_id=hotel_id)


@router.post(
    path="",
    summary="Создание номера",
    description="Создание номера для отеля",
)
async def create_room(
        hotel_id: int = Path(description="Айди отеля"),
        room_data: RoomAddRequest = Body(
            openapi_examples={
                "1": room_standart,
            }
        )
):
    async with async_session_maker() as session:
        _room_data = RoomAdd(hotel_id=hotel_id,**room_data.model_dump())
        result = await RoomsRepository(session).add(_room_data)
        await session.commit()
        return {"status": "OK", "room": result}


@router.get(
    path="/{room_id}",
    summary="Получение номера",
    description="Получить номер по id",
)
async def get_room_by_id(
        hotel_id: int = Path(description="Айди отеля"),
        room_id: int = Path(description="Айди номера")
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id,)


@router.put(
    path="/{room_id}",
    summary="Изменить номер по id",
    description="Изменить все параметры номера по id",
)
async def put_room(
        hotel_id: int = Path(description="Айди отеля"),
        room_id: int = Path(description="Айди номера"),
        room_data: RoomAddRequest = Body(
            openapi_examples={
                "1": room_standart,
            }
        )
):
    async with async_session_maker() as session:
        _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump())
        await RoomsRepository(session).edit(
            id=room_id,
            hotel_id=hotel_id,
            model_data=_room_data,
        )
        await session.commit()
        return {"status": "OK"}

@router.patch(
    path="/{room_id}",
    summary="Изменить номер по id",
    description="Изменить некоторые параметры номера по id",
)
async def edit_room(
        hotel_id: int = Path(description="Айди отеля"),
        room_id: int = Path(description="Айди номера"),
        room_data: RoomPatchRequest = Body(
            openapi_examples={
                "1": room_standart,
            }
        )
):
    async with async_session_maker() as session:
        _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump())
        await RoomsRepository(session).edit(
            model_data=_room_data,
            id=room_id,
            hotel_id=hotel_id,
            exclude_unset=True,
        )
        await session.commit()
        return {"status": "OK"}


@router.delete(
    path="/{room_id}",
    summary="Удаление номера по id",
    description="Удаление уже существующего номера без привязки к отелю",
)
async def delete_room(
        hotel_id: int = Path(description="Айди отеля"),
        room_id: int = Path(description="Айди номера")
):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        if result == 200:
            await session.commit()
            return {"status": "OK"}
        elif result == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"status": "Error - NOT_FOUND"})
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"status": "Error - BAD_REQUEST"})