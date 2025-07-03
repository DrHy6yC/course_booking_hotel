from src.repositories.bookings import BookingsRepository
from src.repositories.facilities import (
    FacilitiesRepository,
    RoomsFacilitiesRepository,
)
from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.repositories.users import UsersRepository


class DBManager:
    def __init__(self, session_factories):
        self.session_factories = session_factories

    async def __aenter__(self):
        self.session = self.session_factories()

        self.bookings = BookingsRepository(self.session)
        self.facilities = FacilitiesRepository(self.session)
        self.hotels = HotelsRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.rooms_facilities = RoomsFacilitiesRepository(self.session)
        self.users = UsersRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
