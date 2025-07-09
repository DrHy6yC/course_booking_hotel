from datetime import date

from sqlalchemy import Select, func, select

from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM


def unoccupied_rooms(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
) -> Select:
    rooms_count = (
        select(BookingsORM.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsORM)
        .filter(
            BookingsORM.date_from <= date_to,
            BookingsORM.date_to >= date_from,
        )
        .group_by(BookingsORM.room_id)
        .cte(name="rooms_count")
    )

    rooms_left_table = (
        select(
            RoomsORM.id.label("room_id"),
            (
                RoomsORM.quantity
                - func.coalesce(rooms_count.c.rooms_booked, 0)
            ).label("rooms_left"),
        )
        .select_from(RoomsORM)
        .outerjoin(rooms_count, RoomsORM.id == rooms_count.c.room_id)
        .cte(name="rooms_left_table")
    )

    rooms_ids_for_hotel = select(RoomsORM.id).select_from(RoomsORM)
    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel = rooms_ids_for_hotel.subquery(
        name="rooms_ids_for_hotel"
    )

    # TODO: Починить типизацию
    rooms_ids_to_get = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(
            rooms_left_table.c.rooms_left > 0,  # type: ignore
            rooms_left_table.c.room_id.in_(rooms_ids_for_hotel),  # type: ignore
        )
    )
    return rooms_ids_to_get


def add_pagination(
    model,
    query,
    limit: int,
    offset: int,
    title: str | None = None,
    location: str | None = None,
):
    if title:
        query = query.filter(
            func.lower(model.title).contains(title.strip().lower())
        )
    if location:
        query = query.filter(
            func.lower(model.location).contains(location.strip().lower())
        )
    query = query.limit(limit).offset(offset)
    return query
