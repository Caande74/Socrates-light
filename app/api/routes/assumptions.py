from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import authenticated_subject, resolve_runtime_owner
from app.dependencies import require_api_key, db_session
from app.schemas.assumption import AssumptionCreate, AssumptionResponse, AssumptionStatusUpdate
from app.services.assumption_service import (
    create_assumption as service_create_assumption,
    update_assumption_status as service_update_assumption_status,
)

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.post("", response_model=AssumptionResponse)
def create_assumption(
    payload: AssumptionCreate,
    subject: str | None = Depends(authenticated_subject),
    db: Session = Depends(db_session),
):
    payload.owner_id = resolve_runtime_owner(payload.owner_id, subject).owner_id
    return service_create_assumption(db, payload)


@router.patch("/{item_id}/status", response_model=AssumptionResponse)
def patch_assumption_status(
    item_id: str,
    payload: AssumptionStatusUpdate,
    subject: str | None = Depends(authenticated_subject),
    db: Session = Depends(db_session),
):
    payload.owner_id = resolve_runtime_owner(payload.owner_id, subject).owner_id
    item = service_update_assumption_status(db, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assumption not found")
    return item
