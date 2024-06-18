import logging
import socket
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager

import redis
import sqlalchemy
from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from starlette import status

from core import config

from core.schema import metadata


class Database:
    engine = create_async_engine(config.DB_DSN, echo=True)

    @classmethod
    async def get(cls):
        async with cls.engine.connect() as connection:
            yield connection

    @classmethod
    async def init(cls):
        async with Database.engine.connect() as connection:
            await connection.run_sync(metadata.create_all)
            await connection.commit()
        await Database.engine.dispose()


class BaseRepository(ABC):
    @abstractmethod
    def __init__(self, connection: AsyncConnection):
        self.connection = connection

    @classmethod
    async def get_repository(cls):
        try:
            async with Database.engine.connect() as connection:
                yield cls(connection)
        except sqlalchemy.exc.InterfaceError as e:
            logging.exception(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="нет соединения с базой")
        except socket.gaierror as e:
            logging.exception(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="нет соединения с базой")

class Cache:
    @staticmethod
    @asynccontextmanager
    async def get():
        _redis: Redis = await Redis.from_url(config.REDIS_DSN)
        try:
            yield _redis
        except redis.exceptions.ConnectionError:
            logging.error("кэш не работает")
        finally:
            await _redis.close()
