from fastapi import FastAPI

from api import endpoint
from api.models import Profile

app = FastAPI()


@app.get("/get_all_profiles", tags=["Profiles"])
async def _get_all_profiles(
        # credentials: HTTPAuthorizationCredentials = Security(security)
):
    # token = credentials.credentials
    # if auth_handler.decode_token(token):
    return await endpoint.get_all_profiles()


# return status.HTTP_403_FORBIDDEN

@app.post('/add_profile', tags=["Profiles"])
async def _add_profile(data: Profile):
    return await endpoint.add_profile(data)
