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


def list_active_adjustments(db: Session) -> list[Adjustment]:
    return db.query(Adjustment).filter(Adjustment.status == "active").all()