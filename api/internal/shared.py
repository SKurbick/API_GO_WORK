import secrets
import string
import asyncio


async def random_string(num: int = 24):
    return "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(num)
    )

