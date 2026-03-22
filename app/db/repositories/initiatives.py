from sqlalchemy.orm import Session
from app.db.models.initiative import Initiative


def create_initiative(db: Session, payload: dict) -> Initiative:
    item = Initiative(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_initiative(db: Session, item_id: str) -> Initiative | None:
    return db.get(Initiative, item_id)


def list_active_initiatives(db: Session) -> list[Initiative]:
    return db.query(Initiative).filter(Initiative.status == "active").all()