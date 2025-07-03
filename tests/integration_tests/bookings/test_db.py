from datetime import date, timedelta

from src.schemas.booking import BookingAdd, BookingRequestAdd


async def test_add_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        room_id=room_id,
        date_from=date.today(),
        date_to=date.today() + timedelta(days=1),
        user_id=user_id,
        price=2500,
    )
    booking_edit_data = BookingRequestAdd(
        room_id=room_id,
        date_from=date.today() + timedelta(days=1),
        date_to=date.today() + timedelta(days=3),
    )

    added_booking = await db.bookings.add(booking_data)
    await db.commit()
    assert added_booking
    assert (
        added_booking.user_id == user_id and added_booking.room_id == room_id
    )

    received_booking = await db.bookings.get_one_or_none(id=added_booking.id)
    await db.rollback()
    assert received_booking
    assert (
        received_booking.user_id == user_id
        and received_booking.room_id == room_id
        and received_booking.date_from == booking_data.date_from
        and received_booking.date_to == booking_data.date_to
        and received_booking.price == booking_data.price
    )

    await db.bookings.edit(model_data=booking_edit_data, id=added_booking.id)
    await db.commit()
    update_booking = await db.bookings.get_one_or_none(id=added_booking.id)
    await db.rollback()
    assert update_booking
    assert (
        update_booking.user_id == user_id
        and update_booking.room_id == room_id
        and update_booking.date_from == booking_edit_data.date_from
        and update_booking.date_to == booking_edit_data.date_to
        and update_booking.date_from != received_booking.date_from
        and update_booking.date_to != received_booking.date_to
    )

    result = await db.bookings.delete(id=added_booking.id)
    await db.commit()
    assert result == 200
    received_booking = await db.bookings.get_one_or_none(id=added_booking.id)
    await db.rollback()
    assert received_booking is None
