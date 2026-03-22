from uuid import uuid4
from sqlalchemy.orm import Session
from app.db.repositories.assumptions import create_assumption as repo_create_assumption
from app.schemas.assumption import AssumptionCreate


def create_assumption(db: Session, payload: AssumptionCreate):
    data = payload.model_dump()

    if not data.get("id"):
        data["id"] = f"assumption-{uuid4().hex[:12]}"

    if not data.get("title"):
        content = (data.get("content") or "").strip()
        data["title"] = content[:80] if content else "Assumption"

    return repo_create_assumption(db, data)
