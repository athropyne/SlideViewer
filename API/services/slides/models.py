import enum
from enum import auto
from typing import Optional

from pydantic import BaseModel, Field


class UploadModel(BaseModel):
    title: str = Field(max_length=100)
    description: Optional[str] = Field(max_length=3000)
