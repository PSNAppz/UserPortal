from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone: str


class User(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    profile_picture_path: Optional[str]
