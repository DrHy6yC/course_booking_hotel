from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import (
    RoomDataMapper,
    RoomWithRelsDataMapper,
)
from src.repositories.utils import unoccupied_rooms


class RoomsRepository(BaseRepository):
    model = RoomsORM
    mapper = RoomDataMapper

    async def get_filter_by_time(
        self, hotel_id: int, date_from: date, date_to: date
    ):
        filter_id = unoccupied_rooms(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsORM.id.in_(filter_id))
        )
        result = await self.session.execute(query)
        return [
            RoomWithRelsDataMapper.map_to_domain_entity(entity)
            for entity in result.unique().scalars().all()
        ]

    async def get_one_or_none_with_rels(
        self, **filter_by
    ) -> RoomWithRelsDataMapper | None:
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        entity = result.unique().scalars().one_or_none()
        if entity is None:
            return None
        return RoomWithRelsDataMapper.map_to_domain_entity(entity)
