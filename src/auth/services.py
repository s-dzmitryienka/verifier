from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.exceptions import UserAlreadyExists
from auth.models import User
from auth.password import PasswordHelperProtocol
from auth.schemas import UserCreateSchema, UserUpdateSchema
from core.crud_mixin import CRUDMixin


class UserService(CRUDMixin):
    table = User
    create_scheme = UserCreateSchema
    update_scheme = UserUpdateSchema

    password_helper: PasswordHelperProtocol

    async def _get_by_email(self, email: str, session: AsyncSession) -> Optional[table]:
        query = select(self.table).where(self.table.email == email)
        res = await session.execute(query)
        return res.scalars().first()

    async def get_by_email(self, email: str, session: AsyncSession) -> table or HTTPException:
        """ Get user by oid field """
        obj = self._get_by_email(email, session)
        self._check_object(obj)
        return obj

    async def create(
        self,
        input_data: UserCreateSchema,
        session: AsyncSession,
    ) -> User:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param input_data: The UserCreate schema to create.
        :param session: DB async session
        :raises HTTPException(status_code=400): A user already exists with the same e-mail.
        :return: A new user.
        """
        self.validate_password(input_data.password)

        existing_user: Optional[User] = await self._get_by_email(input_data.email, session)
        if existing_user is not None:
            raise UserAlreadyExists

        created_user = await super().create(input_data, session)

        await self.on_after_register(created_user)

        return created_user

    @staticmethod
    def validate_password(password: str) -> None:
        """
        Validate a password.

        :param password: The password to validate.
        :raises InvalidPasswordException: The password is invalid.
        :return: None if the password is valid.
        """
        ...

    async def on_after_register(self, user: table) -> None:
        """
        Perform logic after successful user registration.

        :param user: The registered user
        """
        return  # pragma: no cover
