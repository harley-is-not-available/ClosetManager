from pydantic import BaseModel, EmailStr
from typing import Optional


# User creation schema
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


# User login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# User response schema
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True
