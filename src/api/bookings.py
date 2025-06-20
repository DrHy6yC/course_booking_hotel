from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.booking import BookingAdd, BookingRequestAdd


router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@router.post(
    path="",
    summary="Забронировать номер",
    description="Забронировать номер для активного пользователя"
)
async def create_bookings(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingRequestAdd,
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "Error - Номер не найден"}
        )
    _booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
    result = await db.bookings.add(_booking_data)
    await db.commit()
    return  {"status": "OK", "booking": result}


@router.get(
    path="",
    summary="Получить список всех забронированных номеров",
    description="Получить забронированные номера для всех пользователей"
)
async def get_bookings_me(
        db: DBDep
):
    return await db.bookings.get_all()


@router.get(
    path="/me",
    summary="Получить список забронированных номеров",
    description="Получить забронированные номера активного пользователя"
)
async def get_bookings_me(
        db: DBDep,
        user_id: UserIdDep
):
    return await db.bookings.get_filter_by(user_id=user_id)
