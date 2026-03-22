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


def list_active_decisions(db: Session) -> list[Decision]:
    return db.query(Decision).filter(Decision.status == "active").all()