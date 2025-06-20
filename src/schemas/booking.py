from datetime import date

from pydantic import BaseModel


class BookingRequestAdd(BaseModel):
    date_from: date
    date_to: date


class BookingAdd(BookingRequestAdd):
    room_id: int
    user_id: int
    price: int

class Booking(BookingAdd):
    id: int
