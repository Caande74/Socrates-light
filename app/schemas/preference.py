from typing import Optional
from app.schemas.common import CoreItemCreate, CoreItemResponse


class PreferenceCreate(CoreItemCreate):
    scope: Optional[str] = None


class PreferenceResponse(CoreItemResponse):
    scope: Optional[str] = None

    model_config = {"from_attributes": True}
