from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from src.connectors.database_init import BaseORM

SchemaType = TypeVar("SchemaType", bound=BaseModel)
DBModelType = TypeVar("DBModelType", bound=BaseORM)


class DataMapper(Generic[DBModelType, SchemaType]):
    db_model: Type[DBModelType]
    schema: Type[SchemaType]

    @classmethod
    def map_to_domain_entity(cls, data: DBModelType) -> SchemaType:
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: SchemaType) -> DBModelType:
        return cls.db_model(**data.model_dump())
