import uuid
from uuid import UUID

from core.storages import Cache


class SlideCache(Cache):
    @classmethod
    async def pull(cls, ID: UUID, level: int, row: int, column: int) -> bytes:
        async with Cache.get() as connection:
            return await connection.get(f"{ID}_{level}_{row}_{column}")

    @classmethod
    async def put(cls, ID: UUID, level: int, row: int, column: int, chunk: bytes):
        async with Cache.get() as connection:
            await connection.set(f"{ID}_{level}_{row}_{column}",
                                 chunk,
                                 ex=60 * 30)

    @classmethod
    async def delete(cls, ID: uuid.UUID):
        async with Cache.get() as connection:
            keys = await connection.keys(f"{ID}*")
            await connection.delete(*keys)
