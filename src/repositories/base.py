from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update


class BaseRepository:
    model = None
    schema: BaseModel = None
    def __init__(self, session):
        self.session = session

    async def get_filtered(
            self,
            *filter,
            limit:int = 5,
            offset: int = 0,
            **filter_by
    ):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
            .limit(limit)
            .offset(offset)

        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(obj=model, from_attributes=True) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        entity = result.scalars().one_or_none()
        if entity is None:
            return None
        return self.schema.model_validate(obj=entity, from_attributes=True)

    async def add(
            self,
            model_data: BaseModel,
    ):
        add_model_stmt = insert(self.model).values(**model_data.model_dump()).returning(self.model)
        result = await self.session.execute(add_model_stmt)
        entity = result.scalars().one_or_none()
        return self.schema.model_validate(obj=entity, from_attributes=True)

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
