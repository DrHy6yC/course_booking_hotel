from pydantic import BaseModel, Field


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int


class RoomAdd(RoomAddRequest):
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
