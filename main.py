from fastapi import FastAPI, Depends
from starlette.background import BackgroundTasks
from fastapi.security import OAuth2PasswordBearer

from api import endpoint
from api.models import Profile, UserCreate
from api.internal.auth.auth import _restore_password

app = FastAPI()


@app.get("/get_all_profiles", tags=["Profiles"])
async def _get_all_profiles():
    return await endpoint.get_all_profiles()


@app.post('/add_profile', tags=["Profiles"])
async def _add_profile(data: Profile):
    return await endpoint.add_profile(data)


@app.post("/auth/restore_password/{mail}", tags=["User profile"])
async def restore_password(mail: str):  # +
    return await _restore_password(mail)  # + bg

# @app.post("auth/signup", tags=["Registration"])
# async def signup(
#         user_details: UserCreate
# ):
#     return await _signup(user_details)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}