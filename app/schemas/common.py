from typing import Any, Optional
from uuid import UUID

from app.auth.owners import normalize_owner_id
from pydantic import BaseModel, ConfigDict, Field, field_validator


TagList = list[str] | None


def normalize_tags(value: Any) -> TagList:
    if value is None:
        return None

    if isinstance(value, str):
        tags = [tag.strip() for tag in value.split(",") if tag.strip()]
        return tags or None

    if isinstance(value, list):
        tags = [str(tag).strip() for tag in value if str(tag).strip()]
        return tags or None

    raise TypeError("tags must be null or a list of strings")


def serialize_tags(value: TagList) -> str | None:
    if not value:
        return None
    return ",".join(value)


class RuntimeSchemaBase(BaseModel):
    @field_validator("tags", mode="before", check_fields=False)
    @classmethod
    def validate_tags(cls, value: Any) -> TagList:
        return normalize_tags(value)

    @field_validator("owner_id", mode="before", check_fields=False)
    @classmethod
    def validate_owner_id(cls, value: Any) -> str | None:
        if value is None:
            return None
        if isinstance(value, UUID):
            return str(value)
        return normalize_owner_id(str(value))


class CoreItemCreate(RuntimeSchemaBase):
    id: str = Field(...)
    title: str
    content: str
    status: str = "active"
    tags: TagList = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    owner_id: Optional[str] = None


class CoreItemResponse(CoreItemCreate):
    owner_name: Optional[str] = None
    legacy_owner: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
