from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "InvalidRefreshToken",
    "InvalidScopeToken",
    "InvalidToken",
    "RefreshTokenExpired",
    "TokenExpired",
]


class InvalidScopeToken(BaseAPIException):
    message = "Invalid scope for token."
    status_code = status.HTTP_401_UNAUTHORIZED


class RefreshTokenExpired(BaseAPIException):
    message = "Refresh token expired."
    status_code = status.HTTP_401_UNAUTHORIZED


class InvalidRefreshToken(BaseAPIException):
    message = "Invalid refresh token."
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenExpired(BaseAPIException):
    message = "Token expired."
    status_code = status.HTTP_401_UNAUTHORIZED


class InvalidToken(BaseAPIException):
    message = "Invalid token."
    status_code = status.HTTP_401_UNAUTHORIZED