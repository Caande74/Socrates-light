from sqlalchemy.orm import Session


def create_item(db: Session, model, payload):
    item = model(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_item(db: Session, model, item_id: str):
    return db.get(model, item_id)


def list_active(db: Session, model):
    return db.query(model).filter(model.status == "active").all()
