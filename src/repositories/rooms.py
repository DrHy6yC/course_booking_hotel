from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository



class HotelsRepository(BaseRepository):
    model = RoomsORM
