from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import require_api_key, db_session
from app.schemas.assumption import AssumptionCreate, AssumptionResponse
from app.services.assumption_service import create_assumption as service_create_assumption

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.post("", response_model=AssumptionResponse)
def create_assumption(payload: AssumptionCreate, db: Session = Depends(db_session)):
    return service_create_assumption(db, payload)