"""Module for load settings form `.env` or if server running with parameter
`dev` from `.env.dev`"""

from functools import lru_cache
from typing import List

import pydantic
from dotenv import find_dotenv
from pydantic import EmailStr
from pydantic.env_settings import BaseSettings
from pydantic.types import PositiveInt, SecretStr

__all__ = ["Settings", "get_settings"]


class _Settings(BaseSettings):
    class Config:
        """Configuration of settings."""

        #: str: env file encoding.
        env_file_encoding = "utf-8"
        #: str: allow custom fields in model.
        arbitrary_types_allowed = True


class Settings(_Settings):
    """Server settings.

    Formed from `.env` or `.env.dev`.
    """

    #: SecretStr: secret x-token for authority.
    # X_API_TOKEN: SecretStr

    #: str: Postgresql host.
    POSTGRES_HOST: str
    #: PositiveInt: positive int (x > 0) port of postgresql.
    POSTGRES_PORT: PositiveInt
    #: str: Postgresql user.
    POSTGRES_USER: str
    #: SecretStr: Postgresql password.
    POSTGRES_PASSWORD: SecretStr
    #: str: Postgresql database name.
    POSTGRES_DATABASE_NAME: str
    #: SecretStr: secret for bcrypt
    # SECRET_KEY: SecretStr

    # email
    MAIL_USERNAME: pydantic.EmailStr
    MAIL_PASSWORD: pydantic.SecretStr
    MAIL_FROM: str
    MAIL_PORT: pydantic.PositiveInt
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool
    VALIDATE_CERTS: bool
    # SUPERADMIN_MAILS: List[EmailStr]


@lru_cache()
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""
    return Settings(_env_file=find_dotenv(env_file))