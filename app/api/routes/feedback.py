from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import authenticated_subject, resolve_runtime_owner
from app.dependencies import require_api_key, db_session
from app.schemas.feedback import FeedbackCreate, FeedbackResponse, FeedbackStatusUpdate
from app.services.case_learning_service import (
    create_feedback as service_create_feedback,
    update_feedback_status as service_update_feedback_status,
)

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.post("", response_model=FeedbackResponse)
def create_feedback(
    payload: FeedbackCreate,
    subject: str | None = Depends(authenticated_subject),
    db: Session = Depends(db_session),
):
    payload.owner_id = resolve_runtime_owner(payload.owner_id, subject).owner_id
    return service_create_feedback(db, payload)


@router.patch("/{item_id}/status", response_model=FeedbackResponse)
def patch_feedback_status(
    item_id: str,
    payload: FeedbackStatusUpdate,
    subject: str | None = Depends(authenticated_subject),
    db: Session = Depends(db_session),
):
    payload.owner_id = resolve_runtime_owner(payload.owner_id, subject).owner_id
    item = service_update_feedback_status(db, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    return item
