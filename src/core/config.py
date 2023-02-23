import logging

from pydantic import BaseSettings, PostgresDsn

from core.logger import LOGGING


logging.basicConfig(**LOGGING)


class AppSettings(BaseSettings):
    app_title: str
    database_dsn: PostgresDsn
    app_description: str
    redis_host: str
    redis_port: int
    token_ttl: int
    secret_key: str

    class Config:
        env_file = '.env'


app_settings = AppSettings()
