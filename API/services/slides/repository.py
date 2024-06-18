from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import CursorResult, select
from sqlalchemy.ext.asyncio import AsyncConnection

from core.schema import slides
from core.storages import BaseRepository


class Repository(BaseRepository):

    def __init__(self, connection: AsyncConnection):
        super().__init__(connection)

    async def insert(self,
                     data: dict):
        cursor: CursorResult = await self.connection.execute(slides.insert().values(data).returning(slides))
        await self.connection.commit()
        await self.connection.close()
        return cursor.mappings().one()

    async def get_list(self):
        cursor: CursorResult = await self.connection.execute(
            select(
                slides.c.ID,
                slides.c.title,
                slides.c.description
            )
        )
        return cursor.mappings().fetchall()

    async def get_by_id(self, ID: UUID):
        cursor: CursorResult = await self.connection.execute(
            select(
                slides.c.ID,
                slides.c.title,
                slides.c.description
            ).where(slides.c.ID == ID)
        )
        return cursor.mappings().fetchone()

    async def update(self, ID: UUID, data: dict):
        cursor: CursorResult = await self.connection.execute(
            slides.update().values(data).where(slides.c.ID == ID)
        )
        if cursor.rowcount != 1:
            raise HTTPException(status_code=404)
        await self.connection.commit()
        await self.connection.close()

    async def delete(self, ID: UUID):
        cursor: CursorResult = await self.connection.execute(
            slides.delete().where(slides.c.ID == ID)
        )
        await self.connection.commit()
        await self.connection.close()
