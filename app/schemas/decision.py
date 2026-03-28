from typing import Optional
from app.schemas.common import CoreItemCreate, CoreItemResponse, validate_status
from pydantic import field_validator


class DecisionCreate(CoreItemCreate):
    decision_date: Optional[str] = None
    rationale: Optional[str] = None
    impact_scope: Optional[str] = None

    @field_validator("status", mode="before")
    @classmethod
    def validate_item_status(cls, value: Optional[str]) -> str:
        return validate_status(value)


class DecisionResponse(CoreItemResponse):
    decision_date: Optional[str] = None
    rationale: Optional[str] = None
    impact_scope: Optional[str] = None

    model_config = {"from_attributes": True}
