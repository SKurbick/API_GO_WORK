from datetime import datetime, timedelta

from api.endpoint import send_email
from api.settings import settings
from api import endpoint
from api.database import db_connect
from api.internal.auth.auth import user_get_by_mail
from api.internal.shared import random_string
from api.models import Profile, UserCreate, User, UserInDB, Token, TokenData, EmailSchemaForRestore
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Union, Dict, Any, Optional
from fastapi import BackgroundTasks, Request, Depends, status

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

# время на обновление токена
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI()
hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/get_all_profiles", tags=["Profiles"])
async def _get_all_profiles():
    return await endpoint.get_all_profiles()


@app.post('/add_profile', tags=["Profiles"])
async def _add_profile(data: Profile):
    return await endpoint.add_profile(data)


@app.post("/auth/restore_password/{mail}", tags=["User profile"])
async def restore_password(mail: str):  # +
    return await _restore_password(mail)  # + bg

def verify_password(plain_password, hashed_password):
    return hasher.verify(plain_password, hashed_password)


def encode_password(password):
    return hasher.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt





@app.post("/auth/restore_password/{mail}", tags=["User profile"])
async def restore_password(mail: str, bg: BackgroundTasks):
    return await _restore_password(mail, bg)
