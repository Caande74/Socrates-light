from sqlalchemy.orm import Session
from app.runtime.statuses import RETRIEVABLE_STATUSES


def create_item(db: Session, model, payload):
    item = model(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_item(db: Session, model, item_id: str):
    return db.get(model, item_id)


def list_active(db: Session, model, owner_id: str | None = None):
    query = db.query(model).filter(model.status == "active")
    if owner_id is not None and hasattr(model, "owner_id"):
        query = query.filter(model.owner_id == owner_id)
    return query.all()


def list_retrievable(db: Session, model, owner_id: str | None = None):
    query = db.query(model).filter(model.status.in_(RETRIEVABLE_STATUSES))
    if owner_id is not None and hasattr(model, "owner_id"):
        query = query.filter(model.owner_id == owner_id)
    return query.all()


def update_item_status(db: Session, model, item_id: str, status: str, owner_id: str | None = None):
    query = db.query(model).filter(model.id == item_id)
    if owner_id is not None and hasattr(model, "owner_id"):
        query = query.filter(model.owner_id == owner_id)

    item = query.first()
    if item is None:
        return None

    item.status = status
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
