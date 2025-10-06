from __future__ import annotations
from pydantic import BaseModel, EmailStr, field_validator
from typing import List
from datetime import datetime

# Auth
class RegisterIn(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def strong_enough(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Users
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

# Posts
class PostCreate(BaseModel):
    title: str
    content: str

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    owner_id: int

class MeOut(BaseModel):
    user: UserOut
    posts: List[PostOut]
