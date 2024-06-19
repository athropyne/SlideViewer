import uuid
from typing import Optional

from pydantic import BaseModel, Field


class UploadModel(BaseModel):
    title: str = Field(max_length=100)
    description: Optional[str] = Field(max_length=3000)


class UpdateModel(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=3000)


class OutSlideInfoModel(BaseModel):
    ID: uuid.UUID
    title: str
    description: Optional[str]
    original_name: str
    ext: str

class OutSlideDimensionsModel(BaseModel):
    width: int
    height: int
