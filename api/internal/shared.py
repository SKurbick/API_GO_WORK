import secrets
import string
import asyncio


async def random_string(num: int = 24):
    return "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(num)
    )


loop = asyncio.run(random_string(num=10))
print(loop)
