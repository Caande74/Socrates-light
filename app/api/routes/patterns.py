from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import require_api_key, db_session
from app.schemas.pattern import PatternCreate, PatternResponse
from app.services.case_learning_service import create_pattern as service_create_pattern

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.post("", response_model=PatternResponse)
def create_pattern(payload: PatternCreate, db: Session = Depends(db_session)):
    return service_create_pattern(db, payload)