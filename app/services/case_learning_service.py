import logging
from uuid import uuid4
from sqlalchemy.orm import Session

from app.auth.owners import resolve_owner_context
from app.db.repositories.case_outcomes import create_case_outcome as repo_create_case_outcome
from app.db.repositories.feedback import (
    create_feedback as repo_create_feedback,
    find_active_feedback_by_content,
    update_feedback_status as repo_update_feedback_status,
)
from app.db.repositories.adjustments import create_adjustment as repo_create_adjustment
from app.db.repositories.patterns import create_pattern as repo_create_pattern

from app.schemas.case_outcome import CaseOutcomeCreate
from app.schemas.common import serialize_tags
from app.schemas.feedback import FeedbackCreate, FeedbackStatusUpdate
from app.schemas.adjustment import AdjustmentCreate
from app.schemas.pattern import PatternCreate

logger = logging.getLogger(__name__)


def _apply_owner_context(data: dict) -> dict:
    owner_context = resolve_owner_context(owner_id=data["owner_id"], legacy_owner=data.get("legacy_owner"))
    data["owner_id"] = owner_context.owner_id
    data["owner_name"] = owner_context.owner_name
    data["legacy_owner"] = owner_context.legacy_owner
    return data


def create_case_outcome(db: Session, payload: CaseOutcomeCreate):
    data = payload.model_dump()
    return repo_create_case_outcome(db, data)


def create_feedback(db: Session, payload: FeedbackCreate):
    data = payload.model_dump()
    data["tags"] = serialize_tags(data.get("tags"))
    data = _apply_owner_context(data)

    if not data.get("id"):
        data["id"] = f"feedback-{uuid4().hex[:12]}"

    if not data.get("title"):
        content = (data.get("content") or "").strip()
        data["title"] = content[:80] if content else "Feedback"

    existing = find_active_feedback_by_content(db, data["content"], data["owner_id"])
    if existing:
        return existing

    logger.info("runtime_feedback_create owner_id=%s owner_name=%s", data["owner_id"], data["owner_name"])
    return repo_create_feedback(db, data)


def update_feedback_status(db: Session, item_id: str, payload: FeedbackStatusUpdate):
    data = payload.model_dump()
    owner_context = resolve_owner_context(owner_id=data["owner_id"])
    return repo_update_feedback_status(db, item_id, data["status"], owner_context.owner_id)


def create_adjustment(db: Session, payload: AdjustmentCreate):
    data = payload.model_dump()
    data["tags"] = serialize_tags(data.get("tags"))
    data = _apply_owner_context(data)

    if not data.get("id"):
        data["id"] = f"adjustment-{uuid4().hex[:12]}"

    if not data.get("title"):
        content = (data.get("content") or "").strip()
        data["title"] = content[:80] if content else "Adjustment"

    logger.info("runtime_adjustment_create owner_id=%s owner_name=%s", data["owner_id"], data["owner_name"])
    return repo_create_adjustment(db, data)


def create_pattern(db: Session, payload: PatternCreate):
    data = payload.model_dump()
    data["tags"] = serialize_tags(data.get("tags"))
    data = _apply_owner_context(data)

    if not data.get("id"):
        data["id"] = f"pattern-{uuid4().hex[:12]}"

    if not data.get("title"):
        content = (data.get("content") or "").strip()
        data["title"] = content[:80] if content else "Pattern"

    logger.info("runtime_pattern_create owner_id=%s owner_name=%s", data["owner_id"], data["owner_name"])
    return repo_create_pattern(db, data)
