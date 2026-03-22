from typing import Optional
from app.schemas.common import CoreItemResponse
from pydantic import BaseModel


class AdjustmentCreate(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    content: str
    status: str = "active"
    tags: Optional[str] = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    owner: Optional[str] = None
    target_scope: Optional[str] = None
    target_name: Optional[str] = None
    adjustment_type: Optional[str] = None
    instruction_delta: Optional[str] = None


class AdjustmentResponse(CoreItemResponse):
    target_scope: Optional[str] = None
    target_name: Optional[str] = None
    adjustment_type: Optional[str] = None
    instruction_delta: Optional[str] = None

    model_config = {"from_attributes": True}