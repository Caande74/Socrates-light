import logging
from uuid import uuid4
from sqlalchemy.orm import Session
from app.auth.owners import resolve_owner_context
from app.db.repositories.assumptions import create_assumption as repo_create_assumption
from app.schemas.common import serialize_tags
from app.schemas.assumption import AssumptionCreate

logger = logging.getLogger(__name__)


def create_assumption(db: Session, payload: AssumptionCreate):
    data = payload.model_dump()
    data["tags"] = serialize_tags(data.get("tags"))
    owner_context = resolve_owner_context(owner_id=data["owner_id"], legacy_owner=data.get("legacy_owner"))
    data["owner_id"] = owner_context.owner_id
    data["owner_name"] = owner_context.owner_name
    data["legacy_owner"] = owner_context.legacy_owner

    if not data.get("id"):
        data["id"] = f"assumption-{uuid4().hex[:12]}"

    if not data.get("title"):
        content = (data.get("content") or "").strip()
        data["title"] = content[:80] if content else "Assumption"

    logger.info("runtime_assumption_create owner_id=%s owner_name=%s", data["owner_id"], data["owner_name"])
    return repo_create_assumption(db, data)
