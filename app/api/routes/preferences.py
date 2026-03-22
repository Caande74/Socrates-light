from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import require_api_key, db_session
from app.schemas.preference import PreferenceCreate, PreferenceResponse
from app.services.preference_service import create_preference as service_create_preference

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.post("", response_model=PreferenceResponse)
def create_preference(payload: PreferenceCreate, db: Session = Depends(db_session)):
    return service_create_preference(db, payload)
