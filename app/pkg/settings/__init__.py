from pathlib import Path

from fastapi_mail import ConnectionConfig

from .settings import get_settings

__all__ = (
    'settings',
    'BASE_DIR',
    'config_email',
)

settings = get_settings()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

config_email = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD.get_secret_value(),
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
    TEMPLATE_FOLDER=Path(BASE_DIR,
                         # 'internal',
                         # 'pkg',
                         'templates')

    # TEMPLATE_FOLDER=Path(__file__).parent / 'templates',


    # MAIL_USERNAME=settings.MAIL_USERNAME,
    # MAIL_PASSWORD=settings.MAIL_PASSWORD.get_secret_value(),
    # MAIL_FROM=settings.MAIL_FROM,
    # MAIL_PORT=settings.MAIL_PORT,
    # MAIL_SERVER=settings.MAIL_SERVER,
    # MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    # MAIL_TLS=False,
    # MAIL_SSL=True,
    # USE_CREDENTIALS=True,
    # VALIDATE_CERTS=True,
    # TEMPLATE_FOLDER=Path(
    #     BASE_DIR,
    #     'internal',
    #     'pkg',
    #     'templates')
)
