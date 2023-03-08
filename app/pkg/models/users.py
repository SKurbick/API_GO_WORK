from typing import Optional

from pydantic import SecretStr, EmailStr, BaseModel
from pydantic.fields import Field
from pydantic.types import PositiveInt


class UserFields:
    id = Field(description="id пользователя", example=2)
    email = Field(description='Электронная почта', example='example@example.com')
    password = Field(description='Пароль', example='qwerty')
    name = Field(description='ФИО', example='Ахмедов Ахмед Ахмедович')
    username = Field(description='Никнейм/псевдоним', example='Bubba')
    telegram_profile = Field(description="профиль в телеграм", example="@Durov")


class BaseUser(BaseModel):
    """Base model for user."""


class User(BaseModel):
    id: PositiveInt = UserFields.id
    username: str = UserFields.username
    email: EmailStr = UserFields.email
    name: str = UserFields.name
    telegram_profile: str = UserFields.telegram_profile


class CreateUserCommand(BaseUser):
    email: EmailStr = UserFields.email
    password: SecretStr = UserFields.password
    name: str = UserFields.name
    username: str = UserFields.username
    telegram_profile: str = UserFields.telegram_profile


class UserActivate(CreateUserCommand):
    activate_verification_code: str = None
