from typing import Optional
from app.schemas.common import CoreItemCreate, CoreItemResponse


class GoalCreate(CoreItemCreate):
    horizon: Optional[str] = None


class GoalResponse(CoreItemResponse):
    horizon: Optional[str] = None

    model_config = {"from_attributes": True}