from uuid import UUID

from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    email: str
    name: str

    class Config:
        orm_mode = True


class UserSchema(UserCreateSchema):
    id: UUID
    is_active: bool
