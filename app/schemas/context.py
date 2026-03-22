from pydantic import BaseModel, Field
from app.schemas.common import CoreItemResponse


class ContextRequest(BaseModel):
    query: str
    mode: str | None = None
    role: str | None = None


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