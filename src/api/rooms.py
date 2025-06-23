from datetime import date, timedelta

from fastapi import APIRouter, Body, HTTPException, Path, Query, status

from src.api.dependencies import DBDep
from src.openapi_examples import room_standard
from src.schemas.facility import RoomFacilityAdd
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
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get(
    path="/unoccupied",
    summary="Доступные номера за период",
    description=""
)
async def get_unoccupied_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example=date.today()),
        date_to: date = Query(example=date.today()+timedelta(days=1)),
):
    return await db.rooms.get_filter_by_time(hotel_id=hotel_id,date_from=date_from, date_to=date_to)


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
        )
):
    _room_data = RoomAdd(hotel_id=hotel_id,**room_data.model_dump(exclude={"facilities_ids"}))
    room = await db.rooms.add(_room_data)
    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id,facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "room": room}


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
    return await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id,)


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
        )
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(
        id=room_id,
        hotel_id=hotel_id,
        model_data=_room_data,
    )
    await db.rooms_facilities.set_room_facilities(
        room_id=room_id,
        facilities_ids=room_data.facilities_ids)
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
                "1": room_standard,
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
    if room_data.facilities_ids:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id,
            facilities_ids=room_data.facilities_ids)
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
