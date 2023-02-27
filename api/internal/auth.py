import smtplib
import ssl
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

async def _restore_password(login: str,bg: BackgroundTasks ):# +  bg: BackgroundTasks
    """
    Функция запроса восстановления пароля пользователя
    login: логин пользователя
    """
    # Запрос данных пользователя из БД
    user = await profile_get_by_login(login)
    # Проверка на наличие пользователя с таким логином
    if user is None:
        return HTTPException(status_code=403, detail="User was not found")
    # Проверка статуса аккаунта
    if not user["active"]:
        return HTTPException(status_code=403, detail="User is not active.")
    # Создаем проверочный код и сохраняем в профиль
    restore_code = await random_string(len=8)
    async with db_connect.connect() as conn:
        try:
            await conn.execute(
                "UPDATE public.users " "SET restore_code = $2" "WHERE login = $1;",
                user["login"],
                restore_code,
            )


        except Exception as e:
            print(e)
            return HTTPException(status_code=403, detail="Can not create verification code.")

    smtp_server = "smtp.mail.ru"
    MAIL_USERNAME_test = "malkolm.63.zed@mail.ru"
    MAIL_PASSWORD_test = "2FeynEHRRSHRMxnBFJuw"
    MAIL_RECIPIENT = user["user_mail"]
    print(MAIL_RECIPIENT)
    message = restore_code
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, 587) as server:
        server.starttls(context=context)

        server.login(MAIL_USERNAME_test, MAIL_PASSWORD_test)
        server.sendmail(MAIL_USERNAME_test, MAIL_RECIPIENT, message)
    # Отправка письма пользователю
    # email_schema = EmailSchemaForRestore(
    #     recipient=[user["user_mail"]], restore_code=restore_code,
    #     user_name=user["user_name"], login=user["login"]
    # )
    # await send_email(template_name="restore_pass.html", bg=bg, contents=email_schema)

    return status.HTTP_200_OK
