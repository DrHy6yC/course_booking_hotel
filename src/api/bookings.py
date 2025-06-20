from fastapi import APIRouter

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
    _booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
    result = await db.bookings.add(_booking_data)
    await db.commit()
    return  {"status": "OK", "booking": result}


# @router.post(
#     path="",
#     summary="Получить список забронированных номеров",
#     description="Получить забронированные номера активного пользователя"
# )