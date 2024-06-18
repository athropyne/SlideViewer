import os
import uuid
from io import BytesIO

from core import config
from services.slides import utils
from services.slides.cache import SlideCache
from services.slides.models import UploadModel
from services.slides.repository import Repository
from services.slides.utils import as_form, LocalChunkManager

if hasattr(os, 'add_dll_directory'):
    # Windows
    with os.add_dll_directory(config.openslide_path):
        import openslide
else:
    import openslide
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse, Response

router = APIRouter()


@router.post("/")
async def upload(file: UploadFile,
                 model: UploadModel = Depends(as_form),
                 repository: Repository = Depends(Repository.get_repository)):
    ID = uuid.uuid4()
    file_name, ext = await utils.LocalSlideManager(file).save(str(ID))
    data = dict(ID=ID, original_name=file_name, ext=ext, **model.model_dump())
    result = await repository.insert(data)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@router.get("/")
async def get_list(repository: Repository = Depends(Repository.get_repository)):
    result = await repository.get_list()
    return JSONResponse(
        content=jsonable_encoder(result))


@router.get("/{ID}/info")
async def get_info(ID: uuid.UUID,
                   repository: Repository = Depends(Repository.get_repository)):
    result = await repository.get_by_id(ID)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(result))


@router.get("/{ID}/dimensions")
async def get_dimensions(ID: uuid.UUID):
    try:
        width, height = openslide.OpenSlide(f"{config.SLIDE_PATH}/{ID}").dimensions
        return JSONResponse({"width": width, "height": height})
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/{ID}/{level}/{column}/{row}")
async def get_chunk(ID: uuid.UUID,
                    level: int,
                    column: int,
                    row: int,
                    bg: BackgroundTasks,
                    cache: SlideCache = Depends(SlideCache)
                    ):
    tile = await cache.pull(ID, level, row, column)
    if tile:
        return Response(tile, media_type="image/jpeg")
    chunk_buffer: BytesIO = LocalChunkManager(ID).DZGenerator().tile(level, column, row)
    bg.add_task(cache.put, ID, level, row, column, chunk_buffer.getvalue())
    return Response(chunk_buffer.getvalue(), media_type="image/jpeg", background=bg)


@router.delete("/{ID}")
async def delete(ID: uuid.UUID,
                 bg: BackgroundTasks,
                 repository: Repository = Depends(Repository.get_repository),
                 cache: SlideCache = Depends(SlideCache)
                 ):
    await repository.delete(ID)
    os.remove(os.path.join(config.SLIDE_PATH, str(ID)))
    bg.add_task(cache.delete, ID)
    return Response(status_code=status.HTTP_204_NO_CONTENT, background=bg)
