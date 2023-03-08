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
        fund_service: services.Funds = Depends(Provide[services.Services.fund]),
        funds_users_service: services.FundsUsers = Depends(Provide[services.Services.funds_users])
):
    user = await user_service.create_user(cmd=models.UserActivate.parse_obj(cmd), request=request,
                                          background_task=background_task)
    if cmd.fund:
        fund = await fund_service.read_specific_fund_by_name(models.ReadFundByName(
            name=cmd.fund))
        funds_users = await funds_users_service.create_fund_user(models.CreateFundUserCommand(
            user_id=user.id,
            fund_id=fund.id))
    return user