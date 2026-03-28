from typing import Optional
from app.schemas.common import CoreItemResponse, RuntimeSchemaBase, TagList, validate_status
from pydantic import ConfigDict, Field, field_validator


class AssumptionCreate(RuntimeSchemaBase):
    model_config = ConfigDict(extra="forbid")

    id: Optional[str] = None
    title: Optional[str] = None
    content: str
    status: str = "active"
    tags: TagList = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    owner_id: str | None = Field(default=None, min_length=1)
    falsification_signal: Optional[str] = None
    affected_items: Optional[str] = None

    @field_validator("status", mode="before")
    @classmethod
    def validate_item_status(cls, value: Optional[str]) -> str:
        return validate_status(value, allow_invalid=True)


class AssumptionResponse(CoreItemResponse):
    falsification_signal: Optional[str] = None
    affected_items: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AssumptionStatusUpdate(RuntimeSchemaBase):
    model_config = ConfigDict(extra="forbid")

    owner_id: str | None = Field(default=None, min_length=1)
    status: str

    @field_validator("status", mode="before")
    @classmethod
    def validate_item_status(cls, value: Optional[str]) -> str:
        return validate_status(value, allow_invalid=True)
