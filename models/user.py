from typing import Optional

from sqlmodel import SQLModel, Field


class AuthUser(SQLModel):
    login: str = Field(unique=True)
    password: str


class UpdateUser(SQLModel):
    name: Optional[str] = Field(None, nullable=True)
    password: Optional[str] = Field(None)


class User(AuthUser, UpdateUser, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class CreateUser(User):
    access_token: str

    # class Config:
    #     fields = {"password": {"exclude": True}}
