from datetime import datetime


from pydantic import BaseModel, Field, conint


class UserBase(BaseModel):
    login: str
    name: str
    email: str
    age: conint(ge=0, le=150)


class UserAdd(UserBase):
    password: str


class User(UserBase):
    id: int
    hashed_password: str
    created_at: datetime


class UserPatch(BaseModel):
    login: str | None = Field(default=None)
    name: str | None = Field(default=None)
    email: str | None = Field(default=None)
    age: conint(ge=0, le=150) | None = Field(default=None)
    password: str | None = Field(default=None)
