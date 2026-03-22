from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import require_api_key, db_session
from app.schemas.relationship import RelationshipCreate, RelationshipResponse
from app.services.relationship_service import (
    create_relationship as service_create_relationship,
    list_relationships_for_item as service_list_relationships_for_item,
)

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.post("/link", response_model=RelationshipResponse)
def create_relationship(payload: RelationshipCreate, db: Session = Depends(db_session)):
    return service_create_relationship(db, payload)


@router.get("/{item_type}/{item_id}", response_model=list[RelationshipResponse])
def get_relationships(item_type: str, item_id: str, db: Session = Depends(db_session)):
    return service_list_relationships_for_item(db, item_type, item_id)
