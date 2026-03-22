from sqlalchemy.orm import Session
from app.db.models.relationship import Relationship


def create_relationship(db: Session, payload: dict) -> Relationship:
    item = Relationship(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_relationships_for_item(db: Session, item_type: str, item_id: str) -> list[Relationship]:
    return (
        db.query(Relationship)
        .filter(
            ((Relationship.from_type == item_type) & (Relationship.from_id == item_id))
            | ((Relationship.to_type == item_type) & (Relationship.to_id == item_id))
        )
        .all()
    )
