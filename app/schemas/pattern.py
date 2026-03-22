from typing import Optional
from app.schemas.common import CoreItemResponse
from pydantic import BaseModel


class PatternCreate(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    content: str
    status: str = "active"
    tags: Optional[str] = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    owner: Optional[str] = None
    pattern_type: Optional[str] = None


class PatternResponse(CoreItemResponse):
    pattern_type: Optional[str] = None

    model_config = {"from_attributes": True}