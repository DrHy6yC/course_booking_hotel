from typing import Generic, Type, TypeVar

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from src.exceptions import ObjectNotFoundError
from src.repositories.mappers.base import DataMapper, DBModelType, SchemaType

DataMapperType = TypeVar("DataMapperType", bound=DataMapper)


class BaseRepository(Generic[DBModelType, DataMapperType]):
    model: Type[DBModelType]
    mapper: Type[DataMapperType]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    # TODO: Починить типизацию
    async def get_filtered(
        self, limit: int = 5, offset: int = 0, *filters, **filter_by
    ) -> list[SchemaType]:  # type: ignore
        query = (
            select(self.model)
            .filter(*filters)
            .filter_by(**filter_by)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model)
            for model in result.scalars().all()
        ]

    # TODO: Починить типизацию
    async def get_all(self, *args, **kwargs) -> list[SchemaType]:  # type: ignore
        return await self.get_filtered()

    # TODO: Починить типизацию
    async def get_one_or_none(self, **filter_by) -> SchemaType | None:  # type: ignore
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        entity = result.scalars().one_or_none()
        if entity is None:
            return None
        return self.mapper.map_to_domain_entity(entity)

    async def get_one(self, **filter_by) -> SchemaType:  # type: ignore
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            entity = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundError
        return self.mapper.map_to_domain_entity(entity)

    # TODO: Починить типизацию, вместо SchemaType добавить две схемы,
    #  на входе и на выходе
    async def add(self, model_data: SchemaType) -> SchemaType:  # type: ignore
        add_model_stmt = (
            insert(self.model)
            .values(**model_data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(add_model_stmt)
        entity = result.scalars().one_or_none()
        return self.mapper.map_to_domain_entity(entity)

    async def add_bulk(
        self,
        models_data: list[SchemaType],
    ) -> None:
        add_model_stmt = (
            insert(self.model)
            .values([item.model_dump() for item in models_data])
            .returning(self.model)
        )
        await self.session.execute(add_model_stmt)

    # TODO: Починить типизацию
    async def edit(
        self,
        model_data: SchemaType,  # type: ignore
        exclude_unset: bool = False,
        **filter_by,
    ) -> None:
        edit_model_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**model_data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(edit_model_stmt)

    async def delete(self, **filter_by) -> int:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        count_model = len(result.scalars().all())
        if count_model >= 1:
            delete_model_stmt = delete(self.model).filter_by(**filter_by)
            await self.session.execute(delete_model_stmt)
            return 200
        elif count_model == 0:
            return 404
        else:
            return 400
