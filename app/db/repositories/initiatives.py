from sqlalchemy.orm import Session
from app.db.models.initiative import Initiative
from app.db.repositories.common import update_item_status


def create_initiative(db: Session, payload: dict) -> Initiative:
    item = Initiative(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_initiative(db: Session, item_id: str) -> Initiative | None:
    return db.get(Initiative, item_id)


def list_active_initiatives(db: Session, owner_id: str | None = None) -> list[Initiative]:
    query = db.query(Initiative).filter(Initiative.status == "active")
    if owner_id is not None:
        query = query.filter(Initiative.owner_id == owner_id)
    return query.all()


def update_initiative_status(
    db: Session,
    item_id: str,
    status: str,
    owner_id: str | None = None,
) -> Initiative | None:
    return update_item_status(db, Initiative, item_id, status, owner_id)
