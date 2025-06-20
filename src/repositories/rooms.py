from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.schemas.room import Room


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room
