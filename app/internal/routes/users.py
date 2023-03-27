from typing import List

from fastapi import APIRouter, Depends
from starlette import status
from dependency_injector.wiring import Provide, inject
from starlette.background import BackgroundTasks
from starlette.requests import Request

from app.internal import services
from app.pkg import models

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=models.User,
    status_code=status.HTTP_201_CREATED,
    summary="Create user.",
)
@inject
async def create_user(
        cmd: models.CreateUserCommand,
        request: Request,
        background_task: BackgroundTasks,
        user_service: services.Users = Depends(Provide[services.Services.user]),
):
    user = await user_service.create_user(cmd=models.UserActivate.parse_obj(cmd), request=request,
                                          background_task=background_task)

    return user


@router.get(
    "/",
    response_model=List[models.User],
    status_code=status.HTTP_200_OK,
    summary="Get all users.",
)
@inject
async def get_all_users(
        user_service: services.Users = Depends(Provide[services.Services.user]),
        # is_authorized: bool = Depends(check_jwt),
):
    return await user_service.read_all_users()



