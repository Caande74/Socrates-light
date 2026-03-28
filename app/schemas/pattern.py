from typing import Optional
from app.schemas.common import CoreItemResponse, RuntimeSchemaBase, TagList, validate_status
from pydantic import ConfigDict, Field, field_validator


class PatternCreate(RuntimeSchemaBase):
    model_config = ConfigDict(extra="forbid")

    id: Optional[str] = None
    title: Optional[str] = None
    content: str
    status: str = "active"
    tags: TagList = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    owner_id: str | None = Field(default=None, min_length=1)
    pattern_type: Optional[str] = None

    @field_validator("status", mode="before")
    @classmethod
    def validate_item_status(cls, value: Optional[str]) -> str:
        return validate_status(value)


class PatternResponse(CoreItemResponse):
    pattern_type: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
