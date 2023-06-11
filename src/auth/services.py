from typing import Union, Optional

from auth.models import User
from auth.schemas import UserCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from core.mixins import CRUDMixin


async def create_user(db_session: AsyncSession, user: UserCreateSchema) -> User:
    fake_hashed_password = user.email + "notreallyhashed"
    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=fake_hashed_password,
    )
    db_session.add(db_user)
    await db_session.commit()
    await db_session.refresh(db_user)
    return db_user


class UserService(CRUDMixin):
    table = User
    create_scheme = UserCreateSchema
    update_scheme = UserCreateSchema

    async def validate_password(
        self, password: str, user: Union[create_scheme, update_scheme]
    ) -> None:
        """
        Validate a password.

        *You should overload this method to add your own validation logic.*

        :param password: The password to validate.
        :param user: The user associated to this password.
        :raises InvalidPasswordException: The password is invalid.
        :return: None if the password is valid.
        """
        return  # pragma: no cover

    async def on_after_register(
        self, user: table, request: Optional[Request] = None
    ) -> None:
        """
        Perform logic after successful user registration.

        *You should overload this method to add your own logic.*

        :param user: The registered user
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        """
        return  # pragma: no cover
