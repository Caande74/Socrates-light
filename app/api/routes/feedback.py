from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import require_api_key, db_session
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.services.case_learning_service import create_feedback as service_create_feedback

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.post("", response_model=FeedbackResponse)
def create_feedback(payload: FeedbackCreate, db: Session = Depends(db_session)):
    return service_create_feedback(db, payload)