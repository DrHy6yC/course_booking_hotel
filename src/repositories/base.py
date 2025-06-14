from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update


class BaseRepository:
    model = None
    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(
            self,
            model_data: BaseModel,
    ):
        add_model_stmt = insert(self.model).values(**model_data.model_dump()).returning(self.model)
        result = await self.session.execute(add_model_stmt)
        return result.scalar_one()


    async def edit(
            self,
            model_data: BaseModel,
            exclude_unset: bool = False,
            **filter_by
    ):
        edit_model_stmt = (
            update(self.model).
            filter_by(**filter_by).
            values(**model_data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(edit_model_stmt)


    async def delete(
            self,
            **filter_by
    ):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        count_model = len(result.scalars().all())
        if  count_model== 1:
            delete_model_stmt = delete(self.model).filter_by(**filter_by)
            await self.session.execute(delete_model_stmt)
            return 200
        elif count_model == 0:
            return 404
        else:
            return 400
