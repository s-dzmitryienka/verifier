import sys
from typing import Optional, Tuple

from auth.exceptions import InvalidPasswordException

if sys.version_info < (3, 8):
    from typing_extensions import Protocol  # pragma: no cover
else:
    from typing import Protocol  # pragma: no cover

from passlib import pwd
from passlib.context import CryptContext


class PasswordHelperProtocol(Protocol):
    def verify(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        ...

    def verify_and_update(
        self, plain_password: str, hashed_password: str
    ) -> Tuple[bool, str]:
        ...  # pragma: no cover

    def hash(self, password: str) -> str:
        ...  # pragma: no cover

    def generate(self) -> str:
        ...  # pragma: no cover


class PasswordHelper(PasswordHelperProtocol):
    def __init__(self, context: Optional[CryptContext] = None) -> None:
        if context is None:
            self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        else:
            self.context = context  # pragma: no cover

    def verify(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        return self.context.verify(plain_password, hashed_password)

    def verify_and_update(
        self, plain_password: str, hashed_password: str
    ) -> Tuple[bool, str]:
        return self.context.verify_and_update(plain_password, hashed_password)

    def hash(self, password: str) -> str:
        return self.context.hash(password)

    def generate(self) -> str:
        return pwd.genword()

    @staticmethod
    def validate_password(password: str) -> None:
        """
        Validate a password.

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
