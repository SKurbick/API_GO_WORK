from fastapi import status

from app.pkg.models.base import BaseAPIException

__all__ = (
    'SendingError',
    'EmptyListAddresses',
    'Unknown',
    'NoRights',
    'InvalidRequest',
    'IncorrectData',
    'DepriveError',
    'ActivateError',
)


class SendingError(BaseAPIException):
    message = 'Sending error.'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class EmptyListAddresses(BaseAPIException):
    message = 'There is no one to send mail to. Most likely the list of ' \
              'addresses is empty.'
    status_code = status.HTTP_400_BAD_REQUEST


class NoRights(BaseAPIException):
    message = 'User have not enough rights'
    status_code = status.HTTP_403_FORBIDDEN


class InvalidRequest(BaseAPIException):
    message = 'Invalid request'
    status_code = status.HTTP_403_FORBIDDEN


class IncorrectData(BaseAPIException):
    message = 'Incorrect data'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class DepriveError(BaseAPIException):
    message = 'Error during deprive user'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class ActivateError(BaseAPIException):
    message = 'Error during activate user'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class Unknown(BaseAPIException):
    message = 'An unknown error so far.'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
