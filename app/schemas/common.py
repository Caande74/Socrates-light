from typing import Optional
from pydantic import BaseModel, Field


class CoreItemCreate(BaseModel):
    id: str = Field(...)
    title: str
    content: str
    status: str = "active"
    tags: Optional[str] = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    owner: Optional[str] = None


class CoreItemResponse(CoreItemCreate):
    pass
