from src.connectors.database_init import async_session_maker_null_pool
from src.schemas.hotel import HotelAdd
from src.utils.db_manager import DBManager


async def test_dbmanager_hotel():
    hotel_data = HotelAdd(title="Test Hotel 5 star", location="Сочи ул. Пушкиина 123)")
    async with DBManager(session_factories=async_session_maker_null_pool) as db:
        new_hotel = await db.hotels.add(hotel_data)
        print(new_hotel)
        await db.commit()
