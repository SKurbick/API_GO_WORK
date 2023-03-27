from typing import List

from app.pkg import models
from app.internal.repository.postgresql.cursor import get_cursor
from app.internal.repository.handlers.postgresql.collect_response import collect_response
from app.internal.repository.repository import Repository


class User(Repository):
    @collect_response
    async def create(self, cmd: models.CreateUserCommand) -> models.User:
        create_user = """
            insert into users(
                    email, password, name, username, activate_verification_code, telegram_profile
            )
                values (
                    %(email)s,
                    %(password)s,
                    %(name)s,
                    %(username)s,
                    %(activate_verification_code)s,
                    %(telegram_profile)s
                )
            returning id, email, password, name, username , telegram_profile;
        """
        async with get_cursor() as cur:
            await cur.execute(create_user, cmd.to_dict(show_secrets=True))
            return await cur.fetchone()

    # @collect_response
    # async def read(self, query: models.ReadUserByIdQuery) -> models.User:
    #     q = """
    #         select
    #             id,
    #             email,
    #             password,
    #             name,
    #             username,
    #             display_the_real_name,
    #             phone_number,
    #             photo_id
    #         from users
    #         where users.id = %(id)s
    #     """
    #     async with get_cursor() as cur:
    #         await cur.execute(q, query.to_dict(show_secrets=True))
    #         return await cur.fetchone()

    @collect_response
    async def read_all(self, query: models.ReadAllUsersQuery) -> List[models.User]:
        q = """
            select
                id,
                email,
                password,
                name,
                username,
                telegram_profile
            from users;
        """
        async with get_cursor() as cur:
            await cur.execute(q)
            return await cur.fetchall()
    #
    # @collect_response
    # async def update(self, cmd: models.UpdateUserCommand) -> models.UpdateUserCommand:
    #     q = """
    #         update users
    #             set
    #                 name = %(name)s,
    #                 username = %(username)s,
    #                 display_the_real_name = %(display_the_real_name)s,
    #                 phone_number = %(phone_number)s
    #             where id = %(id)s
    #         returning
    #             id, name, username, display_the_real_name, phone_number;
    #     """
    #     async with get_cursor() as cur:
    #         await cur.execute(q, cmd.to_dict(show_secrets=True))
    #         return await cur.fetchone()
    #
    # @collect_response
    # async def delete(self, cmd: models.DeleteUserCommand) -> models.DeleteUserCommand:
    #     q = """
    #         delete from users where id = %(id)s
    #         returning id
    #     """
    #     async with get_cursor() as cur:
    #         await cur.execute(q, cmd.to_dict(show_secrets=True))
    #         return await cur.fetchone()
    #
    # @collect_response
    # async def read_user_by_email(self, cmd: models.ReadUserByEmail) -> models.UserPassword:
    #     q = """
    #         select
    #             id,
    #             email,
    #             password,
    #             name,
    #             username,
    #             display_the_real_name,
    #             phone_number
    #         from users
    #         where users.email = %(email)s
    #     """
    #     async with get_cursor() as cur:
    #         await cur.execute(q, cmd.to_dict(show_secrets=True))
    #         return await cur.fetchone()
    #
    # @collect_response
    # async def update_password(self, cmd: models.UserPasswordChangeCommand) -> models.UserPasswordChanger:
    #     q = """
    #         update users
    #             set
    #                 password = %(new_password)s
    #             where users.email = %(email)s
    #         returning
    #             email;
    #     """
    #     async with get_cursor() as cur:
    #         await cur.execute(q, cmd.to_dict(show_secrets=True))
    #         return await cur.fetchone()
    #
    # @collect_response
    # async def read_specific_refresh_token(self, query: models.ReadRefreshTokenById) -> models.RefreshTokenDB:
    #     q = """
    #         select
    #             user_id,
    #             refresh_token
    #             from public.user_refresh_tokens
    #         where user_refresh_tokens.user_id = %(user_id)s;
    #     """
    #     async with get_cursor() as cur:
    #         await cur.execute(q, query.to_dict(show_secrets=True))
    #         return await cur.fetchone()
    #
    # @collect_response
    # async def save_refresh_token(self, cmd: models.RefreshTokenSave) -> models.ReadRefreshTokenById:
    #     q = """
    #         insert into public.user_refresh_tokens(user_id, refresh_token)
    #             values (
    #             %(user_id)s,
    #             %(refresh_token)s)
    #         returning user_id
    #     """
    #     async with get_cursor() as cur:
    #         await cur.execute(q, cmd.to_dict(show_secrets=True))
    #         return await cur.fetchone()
    #
    # @collect_response
    # async def update_refresh_token(self, cmd: models.RefreshTokenSave) -> models.ReadRefreshTokenById:
    #     q = """
    #         update public.user_refresh_tokens
    #             set
    #                 refresh_token=%(refresh_token)s
    #         where user_id= %(user_id)s
    #         returning user_id;
    #     """
    #     async with get_cursor() as cur:
    #         await cur.execute(q, cmd.to_dict(show_secrets=True))
    #         return await cur.fetchone()
    #
    # @collect_response
    # async def delete_refresh_token(self, cmd: models.DeleteRefreshToken) -> models.DeleteRefreshToken:
    #     q = """
    #         delete from public.user_refresh_tokens
    #             where user_id= %(user_id)s
    #         returning user_id;
    #     """
    #     async with get_cursor() as cur:
    #         await cur.execute(q, cmd.to_dict(show_secrets=True))
    #         return await cur.fetchone()
    #
    # @staticmethod
    # @collect_response
    # async def activate_checker(query: models.ReadUserByEmail) -> models.UserActivateStatus:
    #     q = """
    #         select
    #             is_activate
    #         from users
    #         where users.email = %(email)s
    #     """
    #     async with get_cursor() as cur:
    #         await cur.execute(q, query.to_dict(show_secrets=True))
    #         return await cur.fetchone()
