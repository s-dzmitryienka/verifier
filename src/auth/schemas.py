from typing import Optional
from uuid import UUID

from pydantic import EmailStr, Field

from auth.password import PasswordHelper
from core.base_schema import BaseSchema


class UserCreateSchema(BaseSchema):
    _include_props = {
        'hashed_password',
    }

    email: EmailStr
    name: str
    password: str = Field(exclude=True)

    @property
    def hashed_password(self) -> str:
        return PasswordHelper().hash(self.password)


class UserUpdateSchema(BaseSchema):
    email: Optional[EmailStr]
    name: Optional[str]


class UserSchema(BaseSchema):
    id: UUID
    email: EmailStr
    name: str
    is_active: bool

    class Config:
        orm_mode = True
