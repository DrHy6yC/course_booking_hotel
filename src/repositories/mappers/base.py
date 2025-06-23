from pydantic import BaseModel

from src.database import BaseORM


class DataMapper:
    db_model = BaseORM
    shema  = BaseModel

    @classmethod
    def map_to_domain_entity(cls, data):
        return  cls.shema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data):
        return  cls.db_model(**data.model_dump())
