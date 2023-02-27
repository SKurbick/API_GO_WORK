from typing import List, Union
from api.settings import settings
from fastapi_mail import MessageSchema, FastMail, ConnectionConfig
from fastapi import status
from fastapi import HTTPException, status, BackgroundTasks, Request
from starlette.responses import JSONResponse
# from fastapi.responses import JSONResponse
from api.database import db_connect
from api.models import Profile, EmailSchema, EmailSchemaForRestore
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD.get_secret_value(),
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_SSL=settings.MAIL_SSL,
    MAIL_TLS=settings.MAIL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
    # TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)

async def get_all_profiles():
    async with db_connect.connect() as conn:
        profiles = await conn.fetch(
            """ 
            SELECT id, first_name, last_name, telegram_link
            FROM reg_users_profile;
            """
        )
        if profiles:
            return await profiles


async def add_profile(data: Profile):
    async with db_connect.connect() as conn:
        await conn.fetch(
            """
        INSERT INTO reg_users_profile (first_name, last_name, telegram_link)
        VALUES ($1, $2, $3);
            """,
            data.first_name, data.last_name, data.telegram_link
        )
        return status.HTTP_200_OK


async def send_email(
        template_name: str,
        bg: BackgroundTasks,
        contents: Union[EmailSchema, EmailSchemaForRestore],
) -> JSONResponse:
    if type(contents) is EmailSchema:
        template_body = {
            'verification_url': contents.verification_url,
            'user_name': contents.user_name,
            'login': contents.login,
        }

    if type(contents) is EmailSchemaForRestore:
        template_body = {
            'restore_code': contents.restore_code,
            'user_name': contents.user_name,
            'login': contents.login,
        }

    message = MessageSchema(
        subject='Требуются действия с учетной записью Terra',
        recipients=contents.recipient,
        template_body=template_body,
    )

    fm = FastMail(conf)

    # await fm.send_message(message, template_name='signin.html') # WORKS ->this works
    bg.add_task(
        fm.send_message, message, template_name=template_name
    )  # DOES NOT WORK -> also works as expected

    return JSONResponse(
        status_code=200,
        content={'message': 'email was sent'},
    )


