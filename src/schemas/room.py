from pydantic import BaseModel, ConfigDict, Field

class RoomBase(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int


class RoomAddRequest(RoomBase):
    facilities_ids: list[int] | None = Field(None)


class RoomAdd(RoomBase):
    hotel_id: int


class Room(RoomAdd):
    id: int


class RoomPatchRequest(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)


class RoomPatch(RoomPatchRequest):
    hotel_id: int | None = Field(None)
