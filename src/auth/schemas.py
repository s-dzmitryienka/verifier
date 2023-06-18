from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from pydantic import EmailStr, Field, validator

from auth.constants import ErrorCode
from auth.exceptions import InvalidPasswordException
from auth.password import PasswordHelper
from core.base_schema import BaseSchema


class UserCreateSchema(BaseSchema):
    _include_props = {
        'hashed_password',
    }

    email: EmailStr
    name: str
    password: str = Field(exclude=True)

    @validator('password')
    def validate_password(cls, v, values, **kwargs):
        try:
            PasswordHelper.validate_password(password=v)
        except InvalidPasswordException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                    "reason": e.reason,
                },
        )
        return v

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
