from sqlalchemy import func, insert, select


from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository



class HotelsRepository(BaseRepository):
    model = HotelsORM

    async def get_all(
            self,
            title,
            location,
            limit,
            offset,
    ):
        query = select(HotelsORM)
        if title:
            query = query.filter(func.lower(HotelsORM.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(HotelsORM.location).contains(location.strip().lower()))
        query = (
            query.
            limit(limit).
            offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
