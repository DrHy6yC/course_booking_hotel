from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repositories.base import BaseRepository
from src.schemas.facility import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomFacility

