from typing import List

from fastapi import status

from api.database import db_connect
from api.models import Profile


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
