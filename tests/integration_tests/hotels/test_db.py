from src.schemas.hotel import HotelAdd


async def test_db_manager_hotel(db):
    hotel_data = HotelAdd(title="Test Hotel 5 star", location="Сочи ул. Пушкиина 123)")
    new_hotel = await db.hotels.add(hotel_data)
    print(new_hotel)
    await db.commit()
