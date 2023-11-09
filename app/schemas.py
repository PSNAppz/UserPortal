from pydantic import BaseModel, EmailStr


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
