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
            **filter_by
    ):
        edit_model_stmt = update(self.model).filter_by(**filter_by).values(**model_data.model_dump())
        await self.session.execute(edit_model_stmt)


    async def delete(
            self,
            **filter_by
    ):
        query_select = select(self.model).filter_by(**filter_by)
        result_select = await self.session.execute(query_select)
        count_model = len(result_select.scalars().all())
        if  count_model== 1:
            query_delete = delete(self.model).filter_by(**filter_by)
            await self.session.execute(query_delete)
            return 200
        elif count_model == 0:
            return 404
        else:
            return 400
