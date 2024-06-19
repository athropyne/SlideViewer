from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import CursorResult, select
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from core.schema import slides
from core.storages import BaseRepository


class Repository(BaseRepository):

    def __init__(self, connection: AsyncConnection):
        super().__init__(connection)

    async def insert(self, data: dict):
        cursor: CursorResult = await self.connection.execute(slides.insert().values(data).returning(slides))
        await self.connection.commit()
        await self.connection.close()
        return cursor.mappings().fetchone()

    async def get_list(self):
        cursor: CursorResult = await self.connection.execute(
            select(
                slides.c.ID,
                slides.c.title,
                slides.c.description
            )
        )
        await self.connection.close()
        return cursor.mappings().fetchall()

    async def get_by_id(self, ID: UUID):
        cursor: CursorResult = await self.connection.execute(
            select(
                slides.c.ID,
                slides.c.title,
                slides.c.description
            ).where(slides.c.ID == ID)
        )
        await self.connection.close()
        result = cursor.mappings().fetchone()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result

    async def update(self, ID: UUID, data: dict):
        cursor: CursorResult = await self.connection.execute(
            slides.update().values(data).where(slides.c.ID == ID).returning(slides)
        )
        await self.connection.commit()
        await self.connection.close()
        if cursor.rowcount != 1:
            raise HTTPException(status_code=404)
        return cursor.mappings().fetchone()

    async def delete(self, ID: UUID):
        cursor: CursorResult = await self.connection.execute(
            slides.delete().where(slides.c.ID == ID)
        )
        await self.connection.commit()
        await self.connection.close()
        if cursor.rowcount != 1:
            raise HTTPException(status_code=404)
