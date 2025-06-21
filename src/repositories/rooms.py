from datetime import date

from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import unoccupied_rooms
from src.schemas.room import Room


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filter_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        return await self.get_filtered(
            RoomsORM.id.in_(
                unoccupied_rooms(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
            )
        )
