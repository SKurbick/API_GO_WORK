from datetime import date, datetime
from typing import Optional, List, Union
from pydantic import BaseModel, EmailStr, AnyHttpUrl, PositiveInt


class Profile(BaseModel):
    # id: int
    first_name: str
    last_name: str
    telegram_link: str


class Report(BaseModel):
    theme: str
    description: str
    conclusion: str
    what_learned: str
    # created_at:


class Language(BaseModel):
    programing_language: str
    profile_id: int
    report_id: int


class EmailSchema(BaseModel):
    recipient: List[EmailStr]
    verification_url: AnyHttpUrl
    user_name: Optional[str] = ""
    login: Optional[str] = ""


class EmailSchemaForRestore(BaseModel):
    recipient: List[EmailStr]
    restore_code: str
    user_name: Optional[str] = ""
    login: Optional[str] = ""
