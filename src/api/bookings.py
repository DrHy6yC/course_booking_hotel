from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.booking import BookingRequestAdd


router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@router.post(
    path="",
    summary="Получить список забронированных номеров",
    description="Получить забронированные номера активного пользователя"
)
async def get_bookings(
        db: DBDep,
):
    pass