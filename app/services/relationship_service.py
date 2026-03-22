from sqlalchemy.orm import Session
from app.db.repositories.relationships import (
    create_relationship as repo_create_relationship,
    list_relationships_for_item as repo_list_relationships_for_item,
)
from app.schemas.relationship import RelationshipCreate


def create_relationship(db: Session, payload: RelationshipCreate):
    data = payload.model_dump()
    return repo_create_relationship(db, data)


def list_relationships_for_item(db: Session, item_type: str, item_id: str):
    return repo_list_relationships_for_item(db, item_type, item_id)