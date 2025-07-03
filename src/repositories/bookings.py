from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import unoccupied_rooms


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsORM).filter(
            BookingsORM.date_from == date.today()
        )
        res = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking)
            for booking in res.scalars().all()
        ]

    async def add_booking(self, model_data: BookingsORM, hotel_id: int):
        filter_id = unoccupied_rooms(
            hotel_id=hotel_id,
            date_from=model_data.date_from,
            date_to=model_data.date_to,
        )
        result = await self.session.execute(filter_id)
        room_ids = result.scalars().all()
        if model_data.room_id in room_ids:
            booking = await self.add(model_data=model_data)
            return booking
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"status": "Error - Все номерa заняты"},
            )
