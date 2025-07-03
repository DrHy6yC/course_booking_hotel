from pydantic import BaseModel
from src.schemas.booking import Booking


class MessageReturn(BaseModel):
    status: str


class MessageReturnBooking(MessageReturn):
    booking: Booking
