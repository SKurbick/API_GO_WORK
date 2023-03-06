from dotenv import find_dotenv
import pydantic


class _Settings(pydantic.BaseSettings):
    class Config:
        env_file_encoding = "utf-8"


class Settings(_Settings):
    # PostgresQL
    POSTGRES_HOSTNAME: str
    POSTGRES_DATABASE: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: pydantic.SecretStr
    POSTGRES_PORT: pydantic.PositiveInt

    # mail
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


def _get_settings() -> Settings:
    settings = Settings(_env_file=find_dotenv(".env"))
    return settings
