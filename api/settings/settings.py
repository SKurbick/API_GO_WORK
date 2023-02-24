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


def _get_settings() -> Settings:
    settings = Settings(_env_file=find_dotenv(".env"))
    return settings
