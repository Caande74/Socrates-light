from typing import Optional
from app.schemas.common import CoreItemCreate, CoreItemResponse


class DecisionCreate(CoreItemCreate):
    decision_date: Optional[str] = None
    rationale: Optional[str] = None
    impact_scope: Optional[str] = None


class DecisionResponse(CoreItemResponse):
    decision_date: Optional[str] = None
    rationale: Optional[str] = None
    impact_scope: Optional[str] = None

    model_config = {"from_attributes": True}