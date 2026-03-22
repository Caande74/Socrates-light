from sqlalchemy.orm import Session
from app.db.models.preference import Preference


def create_preference(db: Session, payload: dict) -> Preference:
    item = Preference(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_preference(db: Session, item_id: str) -> Preference | None:
    return db.get(Preference, item_id)


def list_active_preferences(db: Session, owner_id: str | None = None) -> list[Preference]:
    query = db.query(Preference).filter(Preference.status == "active")
    if owner_id is not None:
        query = query.filter(Preference.owner_id == owner_id)
    return query.all()
