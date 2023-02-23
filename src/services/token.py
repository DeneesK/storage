from aioredis import Redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .common import DBObjectService
from db.db import get_session
from db.redis import get_redis


class TokenService(DBObjectService):
    async def check_token(self, raw_token: str) -> str | None:
        token = raw_token.split(' ')[1]
        if user_id := await self.cache.get(token):
            return user_id


def get_token_service(
        db_session: AsyncSession = Depends(get_session),
        cache: Redis = Depends(get_redis)
) -> TokenService:
    return TokenService(db_session, cache)
