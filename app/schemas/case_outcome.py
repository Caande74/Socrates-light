from typing import Optional
from app.schemas.common import CoreItemCreate, CoreItemResponse


class CaseOutcomeCreate(CoreItemCreate):
    mode: Optional[str] = None
    outcome: Optional[str] = None


class CaseOutcomeResponse(CoreItemResponse):
    mode: Optional[str] = None
    outcome: Optional[str] = None

    model_config = {"from_attributes": True}