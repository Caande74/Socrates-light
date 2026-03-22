from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import require_api_key, db_session
from app.schemas.adjustment import AdjustmentCreate, AdjustmentResponse
from app.services.case_learning_service import create_adjustment as service_create_adjustment

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.post("", response_model=AdjustmentResponse)
def create_adjustment(payload: AdjustmentCreate, db: Session = Depends(db_session)):
    return service_create_adjustment(db, payload)