from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository



class HotelsRepository(BaseRepository):
    model = HotelsORM
