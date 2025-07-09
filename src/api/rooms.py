from datetime import date

from fastapi import APIRouter, Body, HTTPException, Path, Query, status
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import InvalidTimeRangeError, ObjectNotFoundError
from src.openapi_examples import date_today, date_tomorrow, room_standard
from src.schemas.facility import RoomFacilityAdd
from src.schemas.message import MessageReturn
from src.schemas.room import (
    Room,
    RoomAdd,
    RoomAddRequest,
    RoomPatch,
    RoomPatchRequest,
)

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Номера"])


@router.get(
    path="",
    summary="Получение номеров",
    description="Получить все номера в отеле",
)
@cache(expire=10)
async def get_rooms(
    db: DBDep,
    hotel_id: int = Path(description="Айди отеля"),
):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get(
    path="/unoccupied", summary="Доступные номера за период", description=""
)
@cache(expire=10)
async def get_unoccupied_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(openapi_examples={"1": date_today}),
    date_to: date = Query(openapi_examples={"1": date_tomorrow}),
):
    try:
        if date_from > date_to:
            raise InvalidTimeRangeError
    except InvalidTimeRangeError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"status": "ERROR - Дата заезда позже дата выезда"},
        )
    return await db.rooms.get_filter_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


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
            "1": room_standard,
        }
    ),
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "Error - Отель не найден"},
        )
    _room_data = RoomAdd(
        hotel_id=hotel_id, **room_data.model_dump(exclude={"facilities_ids"})
    )
    # TODO: Починить типизацию
    try:
        room: Room = await db.rooms.add(_room_data)  # type: ignore
    except ObjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "Error - Номер не найден"},
        )
    await db.session.flush()

    if room_data.facilities_ids:
        rooms_facilities_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=f_id)
            for f_id in room_data.facilities_ids
        ]
        await db.rooms_facilities.add_bulk(rooms_facilities_data)

    await db.commit()
    return {"status": "OK", "room": room}


@router.get(
    path="/{room_id}",
    summary="Получение номера",
    description="Получить номер по id",
)
@cache(expire=10)
async def get_room_by_id(
    db: DBDep,
    hotel_id: int = Path(description="Айди отеля"),
    room_id: int = Path(description="Айди номера"),
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "Error - Отель не найден"},
        )
    try:
        return await db.rooms.get_one_with_rels(
            id=room_id,
            hotel_id=hotel_id,
        )
    except ObjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "Error - Номер не найден"},
        )


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
            "1": room_standard,
        }
    ),
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "Error - Отель не найден"},
        )
    try:
        await db.rooms.get_one_with_rels(
            id=room_id,
            hotel_id=hotel_id,
        )
    except ObjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "Error - Номер не найден"},
        )
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(
        id=room_id,
        hotel_id=hotel_id,
        model_data=_room_data,
    )
    if room_data.facilities_ids:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=room_data.facilities_ids
        )
    await db.commit()
    return MessageReturn(status="OK")


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
            "1": room_standard,
        }
    ),
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "Error - Отель не найден"},
        )
    try:
        await db.rooms.get_one_with_rels(
            id=room_id,
            hotel_id=hotel_id,
        )
    except ObjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "Error - Номер не найден"},
        )
    _room_data = RoomPatch(
        hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
    )
    await db.rooms.edit(
        model_data=_room_data,
        id=room_id,
        hotel_id=hotel_id,
        exclude_unset=True,
    )
    if room_data.facilities_ids:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=room_data.facilities_ids
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
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "Error - Отель не найден"},
        )
    try:
        await db.rooms.get_one_with_rels(
            id=room_id,
            hotel_id=hotel_id,
        )
    except ObjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "Error - Номер не найден"},
        )
    result = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    if result == 200:
        await db.commit()
        return {"status": "OK"}
    elif result == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "Error - Номер не найден"},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "Error - Неправильный запрос"},
        )
