from uuid import uuid4
from sqlalchemy.orm import Session

from app.db.repositories.case_outcomes import create_case_outcome as repo_create_case_outcome
from app.db.repositories.feedback import (
    create_feedback as repo_create_feedback,
    find_active_feedback_by_content,
)
from app.db.repositories.adjustments import create_adjustment as repo_create_adjustment
from app.db.repositories.patterns import create_pattern as repo_create_pattern

from app.schemas.case_outcome import CaseOutcomeCreate
from app.schemas.feedback import FeedbackCreate
from app.schemas.adjustment import AdjustmentCreate
from app.schemas.pattern import PatternCreate


def create_case_outcome(db: Session, payload: CaseOutcomeCreate):
    data = payload.model_dump()
    return repo_create_case_outcome(db, data)


def create_feedback(db: Session, payload: FeedbackCreate):
    data = payload.model_dump()

    if not data.get("id"):
        data["id"] = f"feedback-{uuid4().hex[:12]}"

    if not data.get("title"):
        content = (data.get("content") or "").strip()
        data["title"] = content[:80] if content else "Feedback"

    existing = find_active_feedback_by_content(db, data["content"])
    if existing:
        return existing

    return repo_create_feedback(db, data)


def create_adjustment(db: Session, payload: AdjustmentCreate):
    data = payload.model_dump()

    if not data.get("id"):
        data["id"] = f"adjustment-{uuid4().hex[:12]}"

    if not data.get("title"):
        content = (data.get("content") or "").strip()
        data["title"] = content[:80] if content else "Adjustment"

    return repo_create_adjustment(db, data)


def create_pattern(db: Session, payload: PatternCreate):
    data = payload.model_dump()

    if not data.get("id"):
        data["id"] = f"pattern-{uuid4().hex[:12]}"

    if not data.get("title"):
        content = (data.get("content") or "").strip()
        data["title"] = content[:80] if content else "Pattern"

    return repo_create_pattern(db, data)