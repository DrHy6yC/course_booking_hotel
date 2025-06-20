from sqlalchemy import func, select

from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository
from src.schemas.hotel import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    async def get_all(
            self,
            title,
            location,
            limit,
            offset,
    ) -> list[Hotel]:
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
        return [Hotel.model_validate(obj=hotel, from_attributes=True) for hotel in result.scalars().all()]
