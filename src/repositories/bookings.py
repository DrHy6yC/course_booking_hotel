from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.schemas.booking import Booking


class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Booking