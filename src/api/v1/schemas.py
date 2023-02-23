from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    access_token: str


class FileInfo(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    path: str
    size: int
    is_downloadable: bool


class UserFiles(BaseModel):
    user_id: str
    files: list[FileInfo]


class Status(BaseModel):
    database: float
    redis: float
