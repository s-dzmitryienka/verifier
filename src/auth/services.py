from typing import Optional, Union

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.exceptions import InvalidPasswordException, UserAlreadyExists
from auth.models import User
from auth.password import PasswordHelperProtocol
from auth.schemas import UserCreateSchema, UserUpdateSchema
from core.crud_mixin import CRUDMixin


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
    def validate_password(password: str) -> None:  # todo: move to pydantic validations!!!
        """
        Validate a password.

        *You should overload this method to add your own validation logic.*

        :param password: The password to validate.
        :raises InvalidPasswordException: The password is invalid.
        :return: None if the password is valid.
        """
        special_chars = {'$', '!', '@', '#', '%', '&'}

        if len(password) < 8:
            msg = 'Password length must be at least 8'
            raise InvalidPasswordException(msg)

        elif len(password) > 18:
            msg = 'Password length must not be greater than 18'
            raise InvalidPasswordException(msg)

        elif not any(char.isdigit() for char in password):
            msg = 'Password should have at least one number'
            raise InvalidPasswordException(msg)

        elif not any(char.isupper() for char in password):
            msg = 'Password should have at least one uppercase letter'
            raise InvalidPasswordException(msg)

        elif not any(char.islower() for char in password):
            msg = 'Password should have at least one lowercase letter'
            raise InvalidPasswordException(msg)

        elif not any(char in special_chars for char in password):
            msg = 'Password should have at least one special character'
            raise InvalidPasswordException(msg)

    async def on_after_register(self, user: table) -> None:
        """
        Perform logic after successful user registration.

        *You should overload this method to add your own logic.*

        :param user: The registered user
        """
        return  # pragma: no cover
