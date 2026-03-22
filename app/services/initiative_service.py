from uuid import uuid4
from sqlalchemy.orm import Session
from app.db.repositories.initiatives import (
    create_initiative as repo_create_initiative,
    list_active_initiatives as repo_list_active_initiatives,
)
from app.schemas.initiative import InitiativeCreate


def create_initiative(db: Session, payload: InitiativeCreate):
    data = payload.model_dump()

    if not data.get("id"):
        data["id"] = f"initiative-{uuid4().hex[:12]}"

    if not data.get("title"):
        content = (data.get("content") or "").strip()
        data["title"] = content[:80] if content else "Initiative"

    return repo_create_initiative(db, data)


def list_active_initiatives(db: Session):
    return repo_list_active_initiatives(db)