from app.database import db_connect
from app.models import Profile, EmailSchema, EmailSchemaForRestore, UserCreate


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
