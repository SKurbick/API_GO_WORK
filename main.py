# from datetime import datetime, timedelta
#
# from app.endpoint import send_email, _restore_password
# from app import endpoint
# from app.models import Profile, UserCreate, User, UserInDB, Token, TokenData, EmailSchemaForRestore
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from fastapi import FastAPI, HTTPException
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from typing import Union, Dict, Any, Optional
# from fastapi import BackgroundTasks, Request, Depends, status
#
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
#
# # время на обновление токена
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
# app = FastAPI()
# hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# @app.get("/get_all_profiles", tags=["Profiles"])
# async def _get_all_profiles():
#     return await endpoint.get_all_profiles()
#
#
# @app.post('/add_profile', tags=["Profiles"])
# async def _add_profile(data: Profile):
#     return await endpoint.add_profile(data)
#
#
# @app.post("/auth/restore_password/{mail}", tags=["User profile"])
# async def restore_password(mail: str, bg: BackgroundTasks):
#     return await _restore_password(mail, bg)
