from typing import Optional
from app.schemas.common import CoreItemResponse
from pydantic import BaseModel


class AssumptionCreate(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    content: str
    status: str = "active"
    tags: Optional[str] = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    owner: Optional[str] = None
    falsification_signal: Optional[str] = None
    affected_items: Optional[str] = None


class AssumptionResponse(CoreItemResponse):
    falsification_signal: Optional[str] = None
    affected_items: Optional[str] = None

    model_config = {"from_attributes": True}