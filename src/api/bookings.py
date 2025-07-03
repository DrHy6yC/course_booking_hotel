from fastapi import APIRouter, HTTPException, status
from fastapi_cache.decorator import cache
from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import AllRoomsBusyError, ObjectNotFoundError
from src.schemas.booking import BookingAdd, BookingRequestAdd
from src.schemas.message import MessageReturn, MessageReturnBooking
from src.schemas.room import Room

router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@router.get(
    path="",
    summary="Получить список всех забронированных номеров",
    description="Получить забронированные номера для всех пользователей",
)
@cache(expire=10)
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get(
    path="/me",
    summary="Получить список забронированных номеров",
    description="Получить забронированные номера активного пользователя",
)
@cache(expire=10)
async def get_bookings_me(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post(
    path="",
    summary="Забронировать номер",
    description="Забронировать номер для активного пользователя",
)
async def create_bookings(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingRequestAdd,
) -> MessageReturnBooking:
    try:
        room: Room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "Error - Номер не найден"},
        )
    _booking_data = BookingAdd(
        user_id=user_id, price=room.price, **booking_data.model_dump()
    )
    try:
        result = await db.bookings.add_booking(
            _booking_data, hotel_id=room.hotel_id
        )
    except AllRoomsBusyError as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"status": ex.detail},
        )
    await db.commit()
    # TODO: Починить типизацию
    return MessageReturnBooking(status="OK", booking=result)  # type: ignore


@router.delete(
    path="/me",
    summary="Удалить бронь",
    description="Удалить забронированные номера активного пользователя",
)
async def delete_bookings(
    db: DBDep,
    user_id: UserIdDep,
) -> MessageReturn:
    await db.bookings.delete(user_id=user_id)
    await db.commit()
    return MessageReturn(status="OK")
