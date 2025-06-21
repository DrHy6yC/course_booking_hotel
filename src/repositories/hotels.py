from datetime import date

from sqlalchemy import func, select

from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import unoccupied_rooms
from src.schemas.hotel import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel


    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            limit: int,
            offset: int,
    ):
        id_unoccupied_rooms = unoccupied_rooms(date_from=date_from, date_to=date_to)
        id_unoccupied_hotels = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(id_unoccupied_rooms))
        )
        return await self.get_filtered(
            HotelsORM.id.in_(id_unoccupied_hotels),
            limit=limit,
            offset=offset,
        )


    async def get_all(
            self,
            title,
            location,
            limit,
            offset,
    ) -> list[Hotel]:
        query = select(HotelsORM)
        if title:
            query = query.filter(func.lower(HotelsORM.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(HotelsORM.location).contains(location.strip().lower()))
        query = (
            query.
            limit(limit).
            offset(offset)
        )
        result = await self.session.execute(query)
        return [Hotel.model_validate(obj=hotel, from_attributes=True) for hotel in result.scalars().all()]
