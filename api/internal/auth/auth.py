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
from api.models import Profile, EmailSchema, EmailSchemaForRestore, UserCreate


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
async def user_add(user_details: UserCreate, hashed_password: str):
    """
    Функция добавляет пользователя в БД
    user_details: информация о пользователе
    hashed_password: hash пароля
    return: True or False
    """
    try:
        async with db_connect.connect() as conn:
            async with conn.transaction():
                result = await conn.cursor(
                    "INSERT INTO public.users("
                    "login, password, user_name, user_mail) "
                    "VALUES ($1, $2, $3, $4) "
                    "RETURNING id;",
                    user_details.login,
                    hashed_password,
                    user_details.user_name,
                    user_details.user_mail,
                )
                res = await result.fetchrow()
                return int(res["id"])
    except Exception:
        return -1


async def user_get_by_mail(user_mail: str):
    """
    Функция ищет пользователя в БД по почте
    user_mail: почта пользователя
    return: None, если пользователь не найден
    return: {"login": login}, если найден
    """
    async with db_connect.connect() as conn:
        users = await conn.fetch(
            """
            SELECT user_name, login, password, active, verification_code, restore_code
            FROM public.users WHERE user_mail = $1 ORDER BY login LIMIT 1
            """,
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
    message = f"ваш логин: {user_mail['login']}\nкод сброса пароля: {restore_code}"
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
            context = ssl.create_default_context()
            server = smtplib.SMTP(smtp_server, 587)
            server.starttls(context=context)
            server.login(MAIL_USERNAME_test, MAIL_PASSWORD_test)
            server.sendmail(MAIL_USERNAME_test, "frenkjust@mail.ru",
                            message.encode())


        except Exception as e:
            print(e)
            return HTTPException(status_code=403, detail="Can not create verification code.")


async def _signup(
        user_details: UserCreate, bg: BackgroundTasks, request: Request
):
    # """
    # Функция регистрации пользователя
    # user_details: информация о пользователе
    # """
    # # Проверка на пустой логин
    # if not user_details.login:
    #     return HTTPException(
    #         status_code=500, detail="Incorrect data for registration"
    #     )
    #
    # # Проверка на пустую почту
    # if not user_details.user_mail:
    #     return HTTPException(
    #         status_code=500, detail="Incorrect data for registration"
    #     )
    #
    # # Проверка на пустое имя
    # if not user_details.user_name:
    #     return HTTPException(
    #         status_code=500, detail="Incorrect data for registration"
    #     )
    #
    # # Проверка на наличие пользователя с таким логином
    # user = await user_get_by_login(user_details.login)
    # if user != None:
    #     return HTTPException(status_code=400, detail="User already exists")
    #
    # # Проверка на наличие пользователя с такой почтой
    # user = await user_get_by_mail(user_details.user_mail)
    # if user != None:
    #     return HTTPException(
    #         status_code=400, detail="User with the same mail already exists"
    #     )

    user_details.verification_code = await random_string()
    verification_url = request.url_for(
        "verify",
        user_login=user_details.login,
        ver_code=user_details.verification_code,
    )

    # Добавление пользователя в БД
    res = -1
    try:
        hashed_password = auth_handler.encode_password(user_details.password)
        res = await user_add(user_details, hashed_password)
    except Exception:
        return HTTPException(
            status_code=500, detail="Incorrect data for registration"
        )

    email_schema = EmailSchema(
        recipient=[user_details.user_mail], verification_url=verification_url
    )
    await send_email(template_name='signin.html', bg=bg, contents=email_schema)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'user_id': res}
    ) if res >= 0 else HTTPException(
        status_code=500, detail="Incorrect data for registration"
    )
