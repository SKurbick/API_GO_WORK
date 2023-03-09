from typing import List, Optional

from pydantic import EmailStr, HttpUrl

from .base import BaseModel

__all__ = [
    'EmailSchema',
    'ActivateUser',
]


class BaseEmail(BaseModel):
    """Base model for user."""


class EmailSchema(BaseEmail):
    recipient: List[EmailStr]
    verification_url: str
    user_email: str


class ActivateUser(BaseEmail):
    recipient: List[EmailStr]
    verification_url: str
