from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload

from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper, RoomDataMapper
from src.repositories.utils import unoccupied_rooms


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsORM).filter(BookingsORM.date_from == date.today())
        res = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()
        ]

    async def add(self, model_data: BookingsORM, hotel_id: int):
        filter_id = unoccupied_rooms(
            hotel_id=hotel_id,
            date_from=model_data.date_from,
            date_to=model_data.date_to,
        )
        query = (
            select(RoomsORM)
            .options(selectinload(RoomsORM.facilities))
            .filter(RoomsORM.id.in_(filter_id))
        )
        result = await self.session.execute(query)
        rooms = [
            RoomDataMapper.map_to_domain_entity(booking)
            for booking in result.scalars().all()
        ]
        if rooms:
            add_model_stmt = (
                insert(self.model)
                .values(**model_data.model_dump())
                .returning(self.model)
            )
            result = await self.session.execute(add_model_stmt)
            entity = result.scalars().one_or_none()
            return self.mapper.map_to_domain_entity(entity)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"status": "Error - Все номерa заняты"},
            )
