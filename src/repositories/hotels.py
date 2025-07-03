from datetime import date

from sqlalchemy import select

from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import add_pagination, unoccupied_rooms
from src.schemas.hotel import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsORM
    mapper = HotelDataMapper

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        title,
        location,
        limit: int,
        offset: int,
    ) -> list[Hotel]:
        id_unoccupied_rooms = unoccupied_rooms(
            date_from=date_from, date_to=date_to
        )
        id_unoccupied_hotels = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(id_unoccupied_rooms))
        )
        id_unoccupied_hotels = add_pagination(
            model=self.model,
            query=id_unoccupied_hotels,
            title=title,
            location=location,
            limit=limit,
            offset=offset,
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
        query = add_pagination(
            model=self.model,
            query=query,
            title=title,
            location=location,
            limit=limit,
            offset=offset,
        )
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(hotel)
            for hotel in result.scalars().all()
        ]
