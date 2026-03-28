from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import authenticated_subject, resolve_runtime_owner
from app.dependencies import require_api_key, db_session
from app.schemas.initiative import InitiativeCreate, InitiativeResponse, InitiativeStatusUpdate
from app.services.initiative_service import (
    create_initiative as service_create_initiative,
    list_active_initiatives as service_list_active_initiatives,
    update_initiative_status as service_update_initiative_status,
)

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.post("", response_model=InitiativeResponse)
def create_initiative(
    payload: InitiativeCreate,
    subject: str | None = Depends(authenticated_subject),
    db: Session = Depends(db_session),
):
    payload.owner_id = resolve_runtime_owner(payload.owner_id, subject).owner_id
    return service_create_initiative(db, payload)


@router.get("/active", response_model=list[InitiativeResponse])
def get_active_initiatives(db: Session = Depends(db_session)):
    return service_list_active_initiatives(db)


@router.patch("/{item_id}/status", response_model=InitiativeResponse)
def patch_initiative_status(
    item_id: str,
    payload: InitiativeStatusUpdate,
    subject: str | None = Depends(authenticated_subject),
    db: Session = Depends(db_session),
):
    payload.owner_id = resolve_runtime_owner(payload.owner_id, subject).owner_id
    item = service_update_initiative_status(db, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Initiative not found")
    return item
