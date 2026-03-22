from typing import Optional
from app.schemas.common import CoreItemResponse, RuntimeSchemaBase, TagList
from pydantic import ConfigDict, Field


class AdjustmentCreate(RuntimeSchemaBase):
    model_config = ConfigDict(extra="forbid")

    id: Optional[str] = None
    title: Optional[str] = None
    content: str
    status: str = "active"
    tags: TagList = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    owner_id: str = Field(..., min_length=1)
    target_scope: Optional[str] = None
    target_name: Optional[str] = None
    adjustment_type: Optional[str] = None
    instruction_delta: Optional[str] = None


class AdjustmentResponse(CoreItemResponse):
    target_scope: Optional[str] = None
    target_name: Optional[str] = None
    adjustment_type: Optional[str] = None
    instruction_delta: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
