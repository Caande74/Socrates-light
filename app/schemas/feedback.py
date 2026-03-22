from typing import Optional
from app.schemas.common import CoreItemResponse
from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    content: str
    status: str = "active"
    tags: Optional[str] = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    owner: Optional[str] = None
    target_type: Optional[str] = None
    target_id: Optional[str] = None
    signal: Optional[str] = None
    severity: Optional[str] = None


class FeedbackResponse(CoreItemResponse):
    target_type: Optional[str] = None
    target_id: Optional[str] = None
    signal: Optional[str] = None
    severity: Optional[str] = None

    model_config = {"from_attributes": True}
