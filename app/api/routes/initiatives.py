from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import require_api_key, db_session
from app.schemas.initiative import InitiativeCreate, InitiativeResponse
from app.services.initiative_service import (
    create_initiative as service_create_initiative,
    list_active_initiatives as service_list_active_initiatives,
)

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.post("", response_model=InitiativeResponse)
def create_initiative(payload: InitiativeCreate, db: Session = Depends(db_session)):
    return service_create_initiative(db, payload)


@router.get("/active", response_model=list[InitiativeResponse])
def get_active_initiatives(db: Session = Depends(db_session)):
    return service_list_active_initiatives(db)