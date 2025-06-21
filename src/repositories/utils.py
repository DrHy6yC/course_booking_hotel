from datetime import date

from sqlalchemy import func, select

from src.database import engine
from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM

def unoccupied_rooms(
        date_from: date,
        date_to: date,
        hotel_id: int | None = None
):
    rooms_hotel = (
        select(RoomsORM.id.label(name="rooms_id"))
        .select_from(RoomsORM)
    )

    if hotel_id is not None:
        rooms_hotel = rooms_hotel.filter(RoomsORM.hotel_id == hotel_id)

    rooms_hotel = rooms_hotel.cte(name="rooms_hotel")

    rooms_count = (
        select(BookingsORM.room_id, func.count("*").label(name="rooms_booked"))
        .select_from(BookingsORM)
        .filter(
            BookingsORM.date_from >= date_from,
            BookingsORM.date_to <= date_to,
            BookingsORM.room_id.in_(
                select(rooms_hotel.c.rooms_id)
                .select_from(rooms_hotel)
            )
        )
        .group_by(BookingsORM.room_id)
        .cte(name="rooms_count")
    )

    rooms_left_table = (
        select(
            RoomsORM.id.label(name="rooms_id"),
            (RoomsORM.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label(name="rooms_left")
        )
        .select_from(rooms_count)
        .outerjoin(RoomsORM, RoomsORM.id == rooms_count.c.room_id)
        .cte(name="rooms_left_table")
    )


    query = select(rooms_left_table.c.rooms_id).select_from(rooms_left_table).filter(rooms_left_table.c.rooms_left > 0)
    print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
    return query