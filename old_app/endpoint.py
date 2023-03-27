# from fastapi import HTTPException, status
# from fastapi_mail import MessageSchema, MessageType, FastMail, ConnectionConfig
# from starlette.background import BackgroundTasks
# from starlette.responses import JSONResponse
# from pathlib import Path
#
# from api.database import db_connect
# from api.internal.auth.auth import user_get_by_mail
# from api.internal.shared import random_string
# from api.models import Profile, EmailSchemaForRestore
# from api.settings import settings
#
# conf = ConnectionConfig(
#     MAIL_USERNAME=settings.MAIL_USERNAME,
#     MAIL_PASSWORD=settings.MAIL_PASSWORD.get_secret_value(),
#     MAIL_FROM=settings.MAIL_FROM,
#     MAIL_PORT=settings.MAIL_PORT,
#     MAIL_SERVER=settings.MAIL_SERVER,
#     MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
#     MAIL_STARTTLS=settings.MAIL_STARTTLS,
#     MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
#     USE_CREDENTIALS=settings.USE_CREDENTIALS,
#     VALIDATE_CERTS=settings.VALIDATE_CERTS,
#
#     TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
#
# )
#
#
# async def get_all_profiles():
#     async with db_connect.connect() as conn:
#         profiles = await conn.fetch(
#             """
#             SELECT id, first_name, last_name, telegram_link
#             FROM reg_users_profile;
#             """
#         )
#         if profiles:
#             return profiles
#
#
# async def add_profile(data: Profile):
#     async with db_connect.connect() as conn:
#         await conn.fetch(
#             """
#         INSERT INTO reg_users_profile (first_name, last_name, telegram_link)
#         VALUES ($1, $2, $3);
#             """,
#             data.first_name, data.last_name, data.telegram_link
#         )
#         return status.HTTP_200_OK
#
#
# async def send_email(template_name: str,
#                      bg: BackgroundTasks,
#                      contents: EmailSchemaForRestore,
#                      ) -> JSONResponse:
#     template_body = {
#         'restore_code': contents.restore_code,
#         'user_name': contents.user_name,
#         'login': contents.login,
#     }
#
#     message = MessageSchema(
#         subject='Требуются действия с учетной записью Terra',
#         recipients=contents.recipient,
#         template_body=template_body,
#         subtype=MessageType.html,
#
#     )
#
#     fm = FastMail(conf)
#     # await fm.send_message(message, template_name="restore_pass.html")
#     bg.add_task(
#         fm.send_message, message, template_name=template_name
#     )
#     return JSONResponse(status_code=200, content={"message": "email has been sent"})
#
#
# async def _restore_password(mail: str, bg: BackgroundTasks):
#     # Запрос данных пользователя из БД
#     user_data = await user_get_by_mail(mail)
#     # Проверка на наличие пользователя с таким логином
#     if user_data is None:
#         return HTTPException(status_code=403, detail="User was not found")
#     # Проверка статуса аккаунта
#     if not user_data["active"]:
#         return HTTPException(status_code=403, detail="User is not active.")
#     # Создаем проверочный код и сохраняем в профиль
#
#     restore_code = await random_string(num=8)
#
#     async with db_connect.connect() as conn:
#         # try:
#         await conn.execute(
#             "UPDATE public.users " "SET restore_code = $2" "WHERE login = $1;",
#             user_data["login"],
#             restore_code,
#         )
#
#     email_schema = EmailSchemaForRestore(
#         recipient=[mail], restore_code=restore_code,
#         user_name=user_data["user_name"], login=user_data["login"]
#     )
#     await send_email(template_name="restore_pass.html", bg=bg, contents=email_schema)
#     return status.HTTP_200_OK
