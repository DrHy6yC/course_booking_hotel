from sqlalchemy import select


class BaseRepository:
    model = None
    def __init__(self, session):
        self.session = session

    async def get_all(
            self
    ):
        query = select(self.model)
                # if title:
                #     query = query.filter(func.lower(HotelsORM.title).contains(title.strip().lower()))
                # if location:
                #     query = query.filter(func.lower(HotelsORM.location).contains(location.strip().lower()))
                # query = (
                #     query.
                #     limit(limit).
                #     offset(offset)
                # )
        result = await self.session.execute(query)
        return result.scalars().all()
