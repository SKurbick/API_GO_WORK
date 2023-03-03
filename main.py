from datetime import datetime, timedelta
from pathlib import Path

from api import endpoint
from api.database import db_connect
from api.internal.auth.auth import user_get_by_mail
from api.internal.auth.terra_auth import _signup
from api.internal.shared import random_string
from api.models import Profile, UserCreate, User, UserInDB, Token, TokenData
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

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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


# @app.post("/auth/signup", tags=["Registration"])
# async def signup(
#         user_details: UserCreate, bg: BackgroundTasks, request: Request
# ):
#     return await _signup(user_details, bg, request)


# @app.get("/items/")
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}


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


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List


class EmailSchemaForRestore(BaseModel):
    recipient: List[EmailStr]
    restore_code: str
    user_name: Optional[str] = ""
    login: Optional[str] = ""


conf = ConnectionConfig(
    MAIL_USERNAME="malkolm.63.zed@mail.ru",
    MAIL_PASSWORD="mYhN9Wmk1H9WMBEyS9gn",
    MAIL_FROM="malkolm.63.zed@mail.ru",
    MAIL_PORT=587,
    # MAIL_USERNAME="terra_test@internet.ru",
    # MAIL_PASSWORD="pMCEpeMSqrgYEPD9pj4s",
    # MAIL_FROM="terra_test@internet.ru",
    # MAIL_PORT=587,
    MAIL_SERVER="smtp.mail.ru",
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    # MAIL_SSL="True",
    # MAIL_TLS="False",

    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',

)

app = FastAPI()


@app.post("/email")
async def send_email(template_name: str,
                     bg: BackgroundTasks,
                     contents: EmailSchemaForRestore,
                     ) -> JSONResponse:
    template_body = {
        'restore_code': contents.restore_code,
        'user_name': contents.user_name,
        'login': contents.login,
    }

    message = MessageSchema(
        subject='Требуются действия с учетной записью Terra',
        recipients=contents.recipient,
        template_body=template_body,
        subtype=MessageType.html,

    )

    fm = FastMail(conf)
    # await fm.send_message(message, template_name="restore_pass.html")
    bg.add_task(
        fm.send_message, message, template_name=template_name
    )
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


async def _restore_password(mail: str, bg: BackgroundTasks):
    # Запрос данных пользователя из БД
    user_data = await user_get_by_mail(mail)
    # Проверка на наличие пользователя с таким логином
    if user_data is None:
        return HTTPException(status_code=403, detail="User was not found")
    # Проверка статуса аккаунта
    if not user_data["active"]:
        return HTTPException(status_code=403, detail="User is not active.")
    # Создаем проверочный код и сохраняем в профиль

    restore_code = await random_string(num=8)

    async with db_connect.connect() as conn:
        # try:
        await conn.execute(
            "UPDATE public.users " "SET restore_code = $2" "WHERE login = $1;",
            user_data["login"],
            restore_code,
        )

    email_schema = EmailSchemaForRestore(
        recipient=[mail], restore_code=restore_code,
        user_name=user_data["user_name"], login=user_data["login"]
    )
    await send_email(template_name="restore_pass.html", bg=bg, contents=email_schema)
    return status.HTTP_200_OK


@app.post("/auth/restore_password/{mail}", tags=["User profile"])
async def restore_password(mail: str, bg: BackgroundTasks):
    return await _restore_password(mail, bg)
