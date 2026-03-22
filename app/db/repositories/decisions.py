from sqlalchemy.orm import Session
from app.db.models.decision import Decision


def create_decision(db: Session, payload: dict) -> Decision:
    item = Decision(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_decision(db: Session, item_id: str) -> Decision | None:
    return db.get(Decision, item_id)


def list_active_decisions(db: Session, owner_id: str | None = None) -> list[Decision]:
    query = db.query(Decision).filter(Decision.status == "active")
    if owner_id is not None:
        query = query.filter(Decision.owner_id == owner_id)
    return query.all()
