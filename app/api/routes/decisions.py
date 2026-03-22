from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import require_api_key, db_session
from app.schemas.decision import DecisionCreate, DecisionResponse
from app.services.decision_service import create_decision as service_create_decision

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.post("", response_model=DecisionResponse)
def create_decision(payload: DecisionCreate, db: Session = Depends(db_session)):
    return service_create_decision(db, payload)
