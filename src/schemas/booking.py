from datetime import date

from pydantic import BaseModel


class BookingRequestAdd(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAdd(BookingRequestAdd):
    user_id: int
    price: int

class Booking(BookingAdd):
    id: int
