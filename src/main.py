import aioredis
import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from db import db, redis
from core.config import app_settings
from api.v1 import main_router


app = FastAPI(
    title=app_settings.app_title,
    description=app_settings.app_description,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json'
)


@app.on_event('startup')
async def on_startup():
    engine = create_async_engine(app_settings.database_dsn, echo=True, future=True)
    db.async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    redis.redis = await aioredis.from_url(f'redis://{app_settings.redis_host}:{app_settings.redis_port}')


@app.on_event('shutdown')
async def on_shutdown():
    await redis.redis.close()
    db.async_session.close_all()


app.include_router(main_router, prefix='/api/v1')


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
