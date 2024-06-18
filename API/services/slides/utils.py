import glob
import logging
import os
import uuid
from abc import ABC, abstractmethod
from functools import lru_cache
from io import BytesIO
from typing import Optional

import aiofiles
from starlette import status

from core import config

if hasattr(os, 'add_dll_directory'):
    # Windows
    with os.add_dll_directory(config.openslide_path):
        import openslide
else:
    import openslide
from fastapi import UploadFile, Form, HTTPException
from openslide.deepzoom import DeepZoomGenerator

from core import config
from services.slides.models import UploadModel


def as_form(
        title: str = Form(max_length=100),
        description: Optional[str] = Form(None, max_length=3000)
):
    return UploadModel(title=title, description=description)


class __SlideManager(ABC):
    def __init__(self, file: UploadFile):
        self.file = file

    @abstractmethod
    async def save(self, file_name: str):
        ext = self.file.filename.split('.')[-1]
        if ext not in [
            "svs",
            "tif",
            "dcm",
            "vms",
            "vmu",
            "ndpi",
            "scn",
            "mrxs",
            "tiff",
            "svsslide",
            "bif",
            "czi"]:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="данный тип файла не поддерживается")
        async with aiofiles.open(f"{config.SLIDE_PATH}{file_name}", "wb") as out_file:
            while content := await self.file.read(1024 ** 2):
                await out_file.write(content)
        return self.file.filename, ext


class LocalSlideManager(__SlideManager):
    async def save(self, file_name: str):
        return await super().save(file_name)
        # ...

    @staticmethod
    async def find(self, ID: uuid.UUID):
        founded_files = glob.glob(os.path.join(config.SLIDE_PATH, f"{ID}.*"))
        if len(founded_files) > 0:
            return founded_files[0]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="слайд не найден"
        )


class LocalChunkManager:
    def __init__(self, slide_id: uuid.UUID):
        self.slide_path = f"{config.SLIDE_PATH}/{slide_id}"
        self.generator: Optional[DeepZoomGenerator] = None

    @lru_cache(maxsize=15)
    def DZGenerator(self):
        try:
            slide = openslide.OpenSlide(self.slide_path)
            self.generator = DeepZoomGenerator(slide)
            return self
        except openslide.lowlevel.OpenSlideUnsupportedFormatError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="слайд не найден"
            )

    @lru_cache(maxsize=30)
    def tile(self, level: int, column: int, row: int) -> BytesIO:
        try:
            tile = self.generator.get_tile(level, (column, row))
            buffer = BytesIO()
            tile.save(buffer, "JPEG")
            buffer.seek(0)
            return buffer
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        except AttributeError:
            logging.error("сначала вызовите DZGenerator!")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
