from datetime import date

from sqlalchemy import select

from src.exceptions import AllRoomsBusyError
from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import unoccupied_rooms
from src.schemas.booking import Booking, BookingAdd


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

    async def add_booking(
        self, model_data: BookingAdd, hotel_id: int
    ) -> Booking | None:
        filter_id = unoccupied_rooms(
            hotel_id=hotel_id,
            date_from=model_data.date_from,
            date_to=model_data.date_to,
        )
        # TODO: переписать на try\except
        result = await self.session.execute(filter_id)
        room_ids = result.scalars().all()
        if model_data.room_id in room_ids:
            booking = await self.add(model_data=model_data)
            return booking  # type: ignore
        else:
            raise AllRoomsBusyError
