class CoreException(Exception):
    pass


class ObjectDoesNotExist(CoreException):
    def __init__(self, reason: str = None) -> None:
        self.reason = reason or 'Object does not exist'
