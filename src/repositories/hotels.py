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
        # Получаем ID свободных комнат
        id_unoccupied_rooms = unoccupied_rooms(
            date_from=date_from, date_to=date_to
        )
        # Получаем ID отелей со свободными комнатами
        id_unoccupied_hotels = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(id_unoccupied_rooms))
        )
        # получаем список отелей
        hotels_query = select(HotelsORM).filter(
            HotelsORM.id.in_(id_unoccupied_hotels)
        )

        query = add_pagination(
            model=self.model,
            query=hotels_query,
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
