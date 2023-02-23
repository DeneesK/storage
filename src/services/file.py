import os
import time
from pathlib import Path
from shutil import make_archive

from aioredis import Redis
from fastapi import Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .common import DBObjectService
from models.db_models import File
from db.db import get_session
from db.redis import get_redis
from core.config import logging


logger = logging.getLogger(__name__)


class FileService(DBObjectService):
    async def upload_file(self, file: UploadFile, path: str, user_id: str) -> File | None:
        size = 0
        if not path:
            path = '.'
        else:
            # creating a new directory called pythondirectory
            Path(path).mkdir(parents=True, exist_ok=True)
        try:
            with open(f'{path}/{file.filename}', 'wb+') as f:
                while contents := file.file.read(1024 * 1024):
                    f.write(contents)
                    size += contents.__sizeof__()
        except Exception as ex:
            logger.error(ex)
            return None
        new_file = File(path=f'{path}/{file.filename}', name=file.filename, user_id=user_id, size=size)
        self.db_session.add(new_file)
        await self.db_session.commit()
        return new_file

    async def get_filelist(self, user_id: str) -> list[File]:
        try:
            files = await self.db_session.execute(
                select(File).where(File.user_id == user_id)
            )
            return files.all()
        except Exception as ex:
            logger.error(ex)

    async def _make_archive(self, compression: str, path: str) -> str:
        root_dir = '/'.join(path.split('/')[:-1])
        base_name = (path.split('/')[-1]).split('.')[0]
        src = os.path.realpath(root_dir)
        path = make_archive(base_name=base_name, base_dir=src, format=compression, root_dir=src)
        return path

    async def get_filepath(self, compression: str | None, file_id: str | None = None, path: str | None = None) -> str:
        if file_id:
            file = await self.db_session.execute(
                select(File).where(File.id == file_id)
            )
            file = file.all()[0][0]
            path = file.path
        if compression:
            path = await self._make_archive(compression, path)
            return path
        return path

    async def ping(self) -> dict:
        start_time = time.time()
        await self.db_session.execute('SELECT 1')
        ping_db = time.time() - start_time
        start_time = time.time()
        await self.cache.get('nothing')
        ping_redis = time.time() - start_time
        return {'database': '{:.4f}'.format(ping_db), 'redis': '{:.4f}'.format(ping_redis)}


def get_file_service(
        db_session: AsyncSession = Depends(get_session),
        cache: Redis = Depends(get_redis)
) -> FileService:
    return FileService(db_session, cache)
