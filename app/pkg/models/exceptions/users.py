from fastapi import status
from fastapi.exceptions import HTTPException

from app.pkg.models.base import BaseAPIException

__all__ = [
    "IncorrectData",
    "UserAlreadyExist",
    "UserNotFound",
    "WrongPassword",
    "Unauthorized",
    "UserNotActivate",
    "UserIsNotModerator",
    "UserIsNotAdmin",
]


class UserAlreadyExist(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    message = "User list already exist."


class UserNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "User was not found."


class WrongPassword(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Wrong password."


class Unauthorized(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Unauthorized."


class IncorrectData(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    message = "Incorrect login data"


class UserNotActivate(BaseAPIException):
    message = "Not activate user"
    status_code = status.HTTP_403_FORBIDDEN


class UserIsNotModerator(BaseAPIException):
    message = "User is not moderator"
    status_code = status.HTTP_403_FORBIDDEN


class UserIsNotAdmin(BaseAPIException):
    message = "User is not moderator"
    status_code = status.HTTP_403_FORBIDDEN


empty = HTTPException(
    status_code=status.HTTP_204_NO_CONTENT,
)