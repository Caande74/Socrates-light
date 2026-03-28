import logging
from uuid import uuid4
from sqlalchemy.orm import Session
from app.auth.owners import resolve_owner_context
from app.db.repositories.initiatives import (
    create_initiative as repo_create_initiative,
    list_active_initiatives as repo_list_active_initiatives,
    update_initiative_status as repo_update_initiative_status,
)
from app.schemas.common import serialize_tags
from app.schemas.initiative import InitiativeCreate, InitiativeStatusUpdate

logger = logging.getLogger(__name__)


def create_initiative(db: Session, payload: InitiativeCreate):
    data = payload.model_dump()
    data["tags"] = serialize_tags(data.get("tags"))
    owner_context = resolve_owner_context(owner_id=data["owner_id"], legacy_owner=data.get("legacy_owner"))
    data["owner_id"] = owner_context.owner_id
    data["owner_name"] = owner_context.owner_name
    data["legacy_owner"] = owner_context.legacy_owner

    if not data.get("id"):
        data["id"] = f"initiative-{uuid4().hex[:12]}"

    if not data.get("title"):
        content = (data.get("content") or "").strip()
        data["title"] = content[:80] if content else "Initiative"

    logger.info("runtime_initiative_create owner_id=%s owner_name=%s", data["owner_id"], data["owner_name"])
    return repo_create_initiative(db, data)


def list_active_initiatives(db: Session):
    return repo_list_active_initiatives(db)


def update_initiative_status(db: Session, item_id: str, payload: InitiativeStatusUpdate):
    data = payload.model_dump()
    owner_context = resolve_owner_context(owner_id=data["owner_id"])
    return repo_update_initiative_status(db, item_id, data["status"], owner_context.owner_id)
