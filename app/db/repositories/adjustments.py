from sqlalchemy.orm import Session
from app.db.models.adjustment import Adjustment


def create_adjustment(db: Session, payload: dict) -> Adjustment:
    item = Adjustment(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_adjustment(db: Session, item_id: str) -> Adjustment | None:
    return db.get(Adjustment, item_id)


def list_active_adjustments(db: Session, owner_id: str | None = None) -> list[Adjustment]:
    query = db.query(Adjustment).filter(Adjustment.status == "active")
    if owner_id is not None:
        query = query.filter(Adjustment.owner_id == owner_id)
    return query.all()
