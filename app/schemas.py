from typing import Literal
from datetime import datetime

from pydantic import BaseModel


# Jobs
class JobBase(BaseModel):
    position: str
    company: str
    location: str
    type: Literal["full-time", "part-time", "internship"] = "full-time"
    status: Literal["pending", "interview", "declined"] = "pending"


class JobCreate(JobBase):
    pass


class JobUpdate(JobBase):
    pass


class JobPublic(JobBase):
    id: int
    create_date: datetime
    user_id: int

    model_config = {"from_attributes": True}

    # class Config:
    #     from_attributes = True


class JobList(BaseModel):
    jobs: list[JobPublic]
    page: int
    pages: int
    total: int


# Users
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int
    is_active: bool
    jobs: list[JobPublic] = []

    model_config = {"from_attributes": True}


class UserList(BaseModel):
    users: list[UserPublic]
    page: int
    pages: int
    total: int


# TOKEN
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# Search Parameters
class SearchParams(BaseModel):
    search: str = ""
    sort: Literal["oldest", "newest", "a-z", "z-a"] = "newest"
    type: Literal["full-time", "part-time", "internship"] | None = None
    status: Literal["pending", "interview", "declined"] | None = None
