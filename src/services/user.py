from pbkdf2 import crypt
from aioredis import Redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .common import DBObjectService
from models.db_models import User
from db.db import get_session
from db.redis import get_redis
from utils.token import get_access_token
from core.config import app_settings


class UserService(DBObjectService):
    password_hash_iterations = 100

    async def _check_password(self, login: str, password: str) -> User | None:
        user = await self.db_session.execute(
            select(User).where(User.login == login)
        )
        user = user.scalar()
        if user and user.password == crypt(password, user.password):
            return user

    async def _to_cache(self, user_id: str, jwt_: str) -> None:
        await self.cache.set(jwt_, user_id, app_settings.token_ttl)

    async def create(self, login: str, password: str) -> User:
        hashed_password = crypt(
            password,
            iterations=self.password_hash_iterations
        )
        new_user = User(login=login, password=hashed_password)
        self.db_session.add(new_user)
        await self.db_session.commit()
        return new_user

    async def login(self, login: str, password: str) -> dict | None:
        user = await self._check_password(login, password)
        if user:
            token = get_access_token(user_id=str(user.id))
            await self._to_cache(str(user.id), token['access_token'])
            return token


def get_user_service(
        db_session: AsyncSession = Depends(get_session),
        cache: Redis = Depends(get_redis)
) -> UserService:
    return UserService(db_session, cache)
