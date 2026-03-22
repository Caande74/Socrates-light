from sqlalchemy.orm import Session
from app.db.models.pattern import Pattern


def create_pattern(db: Session, payload: dict) -> Pattern:
    item = Pattern(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_pattern(db: Session, item_id: str) -> Pattern | None:
    return db.get(Pattern, item_id)


def list_active_patterns(db: Session) -> list[Pattern]:
    return db.query(Pattern).filter(Pattern.status == "active").all()
