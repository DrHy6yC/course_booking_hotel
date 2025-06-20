from fastapi import APIRouter, Body, HTTPException, Path, status

from src.api.dependencies import DBDep
from src.openapi_examples import room_standart
from src.schemas.room import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest


router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Номера"])


@router.get(
    path="",
    summary="Получение номеров",
    description="Получить все номера в отеле",
)
async def get_rooms(
        db: DBDep,
        hotel_id: int = Path(description="Айди отеля"),
):
    return await db.rooms.get_filter_by(hotel_id=hotel_id)


@router.post(
    path="",
    summary="Создание номера",
    description="Создание номера для отеля",
)
async def create_room(
        db: DBDep,
        hotel_id: int = Path(description="Айди отеля"),
        room_data: RoomAddRequest = Body(
            openapi_examples={
                "1": room_standart,
            }
        )
):
    _room_data = RoomAdd(hotel_id=hotel_id,**room_data.model_dump())
    result = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "room": result}


@router.get(
    path="/{room_id}",
    summary="Получение номера",
    description="Получить номер по id",
)
async def get_room_by_id(
        db: DBDep,
        hotel_id: int = Path(description="Айди отеля"),
        room_id: int = Path(description="Айди номера"),
):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id,)


@router.put(
    path="/{room_id}",
    summary="Изменить номер по id",
    description="Изменить все параметры номера по id",
)
async def put_room(
        db: DBDep,
        hotel_id: int = Path(description="Айди отеля"),
        room_id: int = Path(description="Айди номера"),
        room_data: RoomAddRequest = Body(
            openapi_examples={
                "1": room_standart,
            }
        )
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(
        id=room_id,
        hotel_id=hotel_id,
        model_data=_room_data,
    )
    await db.commit()
    return {"status": "OK"}

@router.patch(
    path="/{room_id}",
    summary="Изменить номер по id",
    description="Изменить некоторые параметры номера по id",
)
async def edit_room(
        db: DBDep,
        hotel_id: int = Path(description="Айди отеля"),
        room_id: int = Path(description="Айди номера"),
        room_data: RoomPatchRequest = Body(
            openapi_examples={
                "1": room_standart,
            }
        )
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(
        model_data=_room_data,
        id=room_id,
        hotel_id=hotel_id,
        exclude_unset=True,
    )
    await db.commit()
    return {"status": "OK"}


@router.delete(
    path="/{room_id}",
    summary="Удаление номера по id",
    description="Удаление уже существующего номера без привязки к отелю",
)
async def delete_room(
        db: DBDep,
        hotel_id: int = Path(description="Айди отеля"),
        room_id: int = Path(description="Айди номера"),
):
    result = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    if result == 200:
        await db.commit()
        return {"status": "OK"}
    elif result == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "Error - Номер не найден"}
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "Error - Неправильный запрос"}
        )
