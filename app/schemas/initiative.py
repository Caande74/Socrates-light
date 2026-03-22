from typing import Optional
from app.schemas.common import CoreItemResponse
from pydantic import BaseModel


class InitiativeCreate(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    content: str
    status: str = "active"
    tags: Optional[str] = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    owner: Optional[str] = None
    objective: Optional[str] = None
    stage: Optional[str] = None
    next_step: Optional[str] = None
    blockers: Optional[str] = None


class InitiativeResponse(CoreItemResponse):
    objective: Optional[str] = None
    stage: Optional[str] = None
    next_step: Optional[str] = None
    blockers: Optional[str] = None

    model_config = {"from_attributes": True}