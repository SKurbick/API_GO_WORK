import smtplib
import ssl
from typing import List, Union

from api.internal.shared import random_string
from api.settings import settings
from fastapi_mail import MessageSchema, FastMail, ConnectionConfig
from fastapi import status
from fastapi import HTTPException, status, BackgroundTasks, Request
from starlette.responses import JSONResponse
# from fastapi.responses import JSONResponse
from api.database import db_connect
from api.models import Profile, EmailSchema, EmailSchemaForRestore

# conf = ConnectionConfig(
    # MAIL_USERNAME=settings.MAIL_USERNAME,
    # MAIL_PASSWORD=settings.MAIL_PASSWORD.get_secret_value(),
    # MAIL_FROM=settings.MAIL_FROM,
    # MAIL_PORT=settings.MAIL_PORT,
    # MAIL_SERVER=settings.MAIL_SERVER,
    # MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    # MAIL_SSL=settings.MAIL_SSL,
    # MAIL_TLS=settings.MAIL_TLS,
    # USE_CREDENTIALS=settings.USE_CREDENTIALS,
    # VALIDATE_CERTS=settings.VALIDATE_CERTS,
    # TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
# )


async def user_get_by_mail(user_mail: str):
    """
    Функция ищет пользователя в БД по почте
    user_mail: почта пользователя
    return: None, если пользователь не найден
    return: {"login": login}, если найден
    """
    async with db_connect.connect() as conn:
        users = await conn.fetch(
            f"SELECT login FROM public.users WHERE user_mail = $1 ORDER BY login LIMIT 1",
            user_mail,
        )
        if users:
            return users[0]
        return None


# async def send_email(
#         template_name: str,
#         bg: BackgroundTasks,
#         contents: Union[EmailSchema, EmailSchemaForRestore],
# ) -> JSONResponse:
#     if type(contents) is EmailSchema:
#         template_body = {
#             'verification_url': contents.verification_url,
#             'user_name': contents.user_name,
#             'login': contents.login,
#         }
#
#     if type(contents) is EmailSchemaForRestore:
#         template_body = {
#             'restore_code': contents.restore_code,
#             'user_name': contents.user_name,
#             'login': contents.login,
#         }
#
#     message = MessageSchema(
#         subject='Требуются действия с учетной записью Terra',
#         recipients=contents.recipient,
#         template_body=template_body,
#     )
#
#     fm = FastMail(conf)
#
#     # await fm.send_message(message, template_name='signin.html') # WORKS ->this works
#     bg.add_task(
#         fm.send_message, message, template_name=template_name
#     )  # DOES NOT WORK -> also works as expected
#
#     return JSONResponse(
#         status_code=200,
#         content={'message': 'email was sent'},
#     )


async def _restore_password(mail: str):  # +  bg: BackgroundTasks

    """
    Функция запроса восстановления пароля пользователя
    login: логин пользователя
    """
    # Запрос данных пользователя из БД
    user_mail = await user_get_by_mail(mail)
    # Проверка на наличие пользователя с таким логином
    if user_mail is None:
        return HTTPException(status_code=403, detail="User was not found")
    # Проверка статуса аккаунта
    # if not user_mail["active"]:
    #     return HTTPException(status_code=403, detail="User is not active.")
    # Создаем проверочный код и сохраняем в профиль
    restore_code = await random_string(num=8)
    message = (f"ваш логин: {user_mail['login']}\nкод сброса пароля: {restore_code}")
    print(message)
    async with db_connect.connect() as conn:
        try:
            await conn.execute(
                "UPDATE public.users " "SET restore_code = $2" "WHERE login = $1;",
                user_mail["login"],
                restore_code,
            )

            smtp_server = "smtp.mail.ru"
            MAIL_USERNAME_test = "malkolm.63.zed@mail.ru"
            MAIL_PASSWORD_test = "2FeynEHRRSHRMxnBFJuw"
            # print(mail)
            # print(user_mail['login'])
            # print()
            context = ssl.create_default_context()
            server = smtplib.SMTP(smtp_server, 587)
            print("!!!!")
            server.starttls(context=context)
            server.login(MAIL_USERNAME_test, MAIL_PASSWORD_test)
            server.sendmail(MAIL_USERNAME_test, "frenkjust@mail.ru",
                            message.encode())
            print("!!!!!!!!!!!!!!!!!!!!!!!")


        except Exception as e:
            print(e)
            return HTTPException(status_code=403, detail="Can not create verification code.")
