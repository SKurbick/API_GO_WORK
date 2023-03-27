"""Users service."""
from typing import List, Optional

from starlette import status

from app.internal.services.auth_handler import Auth
from app.internal.repository.postgresql import users
from app.internal.repository import BaseRepository
from app.pkg import models
from app.internal.services.send_email import SendEmail
from app.internal.repository.postgresql.users import User
from app.pkg.models import ActivateUser
from app.pkg.models.exceptions import (
    EmptyResult,
    UniqueViolation,
    UserAlreadyExist,
    UserNotFound,
    WrongPassword,
    IncorrectData,
    SendingError,
    InvalidRequest,
    UserIsNotModerator,
    UserIsNotAdmin, DepriveError,
)

__all__ = (
    'Users',
)

from app.pkg.settings import settings

auth_handler = Auth()
send = SendEmail()


class Users:
    repository: users.User

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def create_user(
            self,
            cmd: models.UserActivate,
            request,
            background_task
    ) -> models.User:
        # try:
        cmd.password = auth_handler.encode_password(cmd.password.get_secret_value())
        # создаем пользователя и верификационный код в бд
        # cmd.activate_verification_code = await SendEmail.random_string()
        user = await self.repository.create(cmd=cmd)
        # ссылка активации
        # try:
        # activate_verification_url = request.url_for(
        #     "verify",
        #     user_email=cmd.email,
        #     ver_code=cmd.activate_verification_code,
        # )
        # email_schema = ActivateUser(
        #     recipient=[cmd.email], verification_url=activate_verification_url,
        # )
        # await send.send_email(template_name='restore_pass.html', background_task=background_task,
        #                       contents=email_schema)
        #     except Exception:
        #         raise SendingError
        return user

    # except UniqueViolation:
    #     raise UserAlreadyExist

    async def read_all_users(
            self,
            query: Optional[models.ReadAllUsersQuery] = None
    ) -> List[models.User]:
        if not query:
            query = models.ReadAllUsersQuery()
        return await self.repository.read_all(query=query)
