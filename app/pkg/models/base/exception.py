__all__ = [
    "BaseAppException",
    "BaseAPIException",
]


class BaseAppException(Exception):
    message: str = ...

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.message}')"


class BaseAPIException(Exception):
    """Exception class for create determinate exception response from API."""

    #: str: Human readable string describing the exception.
    message: str
    #: int: Exception error code.
    status_code: int
