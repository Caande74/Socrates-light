from typing import Optional
from app.schemas.common import CoreItemResponse, RuntimeSchemaBase, TagList
from pydantic import ConfigDict, Field


class InitiativeCreate(RuntimeSchemaBase):
    model_config = ConfigDict(extra="forbid")

    id: Optional[str] = None
    title: Optional[str] = None
    content: str
    status: str = "active"
    tags: TagList = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    owner_id: str = Field(..., min_length=1)
    objective: Optional[str] = None
    stage: Optional[str] = None
    next_step: Optional[str] = None
    blockers: Optional[str] = None


class InitiativeResponse(CoreItemResponse):
    objective: Optional[str] = None
    stage: Optional[str] = None
    next_step: Optional[str] = None
    blockers: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
