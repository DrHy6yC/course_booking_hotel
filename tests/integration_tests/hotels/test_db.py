from src.schemas.hotel import HotelAdd


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Test Hotel 5 star", location="Сочи ул. Пушкиина 123)")
    new_hotel = await db.hotels.add(hotel_data)
    await db.commit()
