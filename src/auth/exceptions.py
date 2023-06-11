from typing import Any

from core.exceptions import CoreException, ObjectDoesNotExist


class UserAlreadyExists(CoreException):
    pass


class UserNotExists(ObjectDoesNotExist):
    pass


class UserInactive(CoreException):
    pass


class InvalidVerifyToken(CoreException):
    pass


class InvalidResetPasswordToken(CoreException):
    pass


class InvalidPasswordException(CoreException):
    def __init__(self, reason: Any) -> None:
        self.reason = reason
