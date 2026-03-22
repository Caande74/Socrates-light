from sqlalchemy.orm import Session


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
