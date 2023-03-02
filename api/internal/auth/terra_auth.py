import smtplib
import ssl
from typing import List, Union

from passlib.context import CryptContext

from api.internal.shared import random_string
from api.settings import settings
from fastapi_mail import MessageSchema, FastMail, ConnectionConfig
from fastapi import status
from fastapi import HTTPException, status, BackgroundTasks, Request
from starlette.responses import JSONResponse
# from fastapi.responses import JSONResponse
from api.database import db_connect
from api.models import Profile, EmailSchema, EmailSchemaForRestore, UserCreate
from datetime import datetime, timedelta
from api import endpoint
from api.models import Profile, UserCreate, User, UserInDB, Token, TokenData
from api.internal.auth.auth import _restore_password
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Union

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

# время на обновление токена
ACCESS_TOKEN_EXPIRE_MINUTES = 30
EXP_REFRESH_TOKEN_HOURS = 24


class Auth:
    hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = settings.SECRET_KEY.get_secret_value()

    def encode_password(self, password):
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password)

    def encode_token(self, username):
        payload = {
            "exp": datetime.utcnow()
                   + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.utcnow(),
            "scope": "access_token",
            "sub": username,
        }
        return jwt.encode(payload, self.secret, algorithm=ALGORITHM)

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[ALGORITHM])
            if payload["scope"] == "access_token":
                return payload["sub"]
            raise HTTPException(
                status_code=401, detail="Scope for the token is invalid"
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def encode_refresh_token(self, username):
        payload = {
            "exp": datetime.utcnow()
                   + timedelta(days=0, hours=EXP_REFRESH_TOKEN_HOURS),
            "iat": datetime.utcnow(),
            "scope": "refresh_token",
            "sub": username,
        }
        return jwt.encode(payload, self.secret, algorithm=ALGORITHM)

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(
                refresh_token, self.secret, algorithms=[ALGORITHM]
            )
            if payload["scope"] == "refresh_token":
                username = payload["sub"]
                new_token = self.encode_token(username)
                return new_token
            raise HTTPException(
                status_code=401, detail="Invalid scope for token"
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")


auth_handler = Auth()


async def _signup(
        user_details: UserCreate, bg: BackgroundTasks, request: Request
):
    """
    Функция регистрации пользователя
    user_details: информация о пользователе
    """
    # Проверка на пустой логин
    if not user_details.login:
        return HTTPException(
            status_code=500, detail="Incorrect data for registration"
        )

    # Проверка на пустую почту
    if not user_details.user_mail:
        return HTTPException(
            status_code=500, detail="Incorrect data for registration"
        )

    # Проверка на пустое имя
    if not user_details.user_name:
        return HTTPException(
            status_code=500, detail="Incorrect data for registration"
        )

    # Проверка на наличие пользователя с таким логином
    user = await user_get_by_login(user_details.login)
    if user != None:
        return HTTPException(status_code=400, detail="User already exists")

    # Проверка на наличие пользователя с такой почтой
    user = await user_get_by_mail(user_details.user_mail)
    if user != None:
        return HTTPException(
            status_code=400, detail="User with the same mail already exists"
        )

    user_details.verification_code = await random_string()
    verification_url = request.url_for(
        "verify",
        user_login=user_details.login,
        ver_code=user_details.verification_code,
    )

    # Добавление пользователя в БД
    res = -1
    try:
        hashed_password = auth_handler.encode_password(user_details.password)
        res = await user_add(user_details, hashed_password)
    except Exception:
        return HTTPException(
            status_code=500, detail="Incorrect data for registration"
        )

    email_schema = EmailSchema(
        recipient=[user_details.user_mail], verification_url=verification_url
    )
    await send_email(template_name='signin.html', bg=bg, contents=email_schema)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'user_id': res}
    ) if res >= 0 else HTTPException(
        status_code=500, detail="Incorrect data for registration"
    )
