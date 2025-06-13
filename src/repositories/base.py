from sqlalchemy import select, insert


class BaseRepository:
    model = None
    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add(
            self,
            model_data,
    ):
        add_hotel_stmt = insert(self.model).values(**model_data.model_dump()).returning(self.model)
        result = await self.session.execute(add_hotel_stmt)
        return result.scalar_one()