from sqlalchemy.orm import Session
from app.db.models.assumption import Assumption


def create_assumption(db: Session, payload: dict) -> Assumption:
    item = Assumption(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_assumption(db: Session, item_id: str) -> Assumption | None:
    return db.get(Assumption, item_id)


def list_active_assumptions(db: Session, owner_id: str | None = None) -> list[Assumption]:
    query = db.query(Assumption).filter(Assumption.status == "active")
    if owner_id is not None:
        query = query.filter(Assumption.owner_id == owner_id)
    return query.all()
