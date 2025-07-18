from pydantic import BaseModel, Field

from src.schemas.facility import Facility


class RoomBase(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int


class RoomAddRequest(RoomBase):
    facilities_ids: list[int] | None = []


class RoomAdd(RoomBase):
    hotel_id: int


class Room(RoomAdd):
    id: int


class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPatchBase(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)


class RoomPatchRequest(RoomPatchBase):
    facilities_ids: list[int] | None = []


class RoomPatch(RoomPatchBase):
    hotel_id: int | None = Field(None)
