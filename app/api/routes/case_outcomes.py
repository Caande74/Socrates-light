from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import require_api_key, db_session
from app.schemas.case_outcome import CaseOutcomeCreate, CaseOutcomeResponse
from app.services.case_learning_service import (
    create_case_outcome as service_create_case_outcome,
)

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.post("", response_model=CaseOutcomeResponse)
def create_case_outcome(payload: CaseOutcomeCreate, db: Session = Depends(db_session)):
    return service_create_case_outcome(db, payload)