from pydantic import BaseModel, Field, field_validator
from app.auth.owners import normalize_owner_id
from app.schemas.common import CoreItemResponse


class ContextRequest(BaseModel):
    query: str
    owner_id: str | None = None
    mode: str | None = None
    role: str | None = None

    @field_validator("owner_id", mode="before")
    @classmethod
    def validate_owner_id(cls, value: str | None) -> str | None:
        return normalize_owner_id(value)


class ContextItemDebug(CoreItemResponse):
    retrieval_path: str
    matched_terms: list[str] = Field(default_factory=list)
    matched_tags: list[str] = Field(default_factory=list)


class ContextGuidance(BaseModel):
    adjustments: list[ContextItemDebug]
    patterns: list[ContextItemDebug]


class ContextResponse(BaseModel):
    query: str
    decisions: list[ContextItemDebug]
    assumptions: list[ContextItemDebug]
    initiatives: list[ContextItemDebug]
    adjustments: list[ContextItemDebug]
    patterns: list[ContextItemDebug]
    feedback: list[ContextItemDebug]
    guidance: ContextGuidance
