from fastapi import FastAPI
from starlette.background import BackgroundTasks

from api import endpoint
from api.models import Profile
from api.internal.auth import _restore_password

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
