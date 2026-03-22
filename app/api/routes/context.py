from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import require_api_key, db_session
from app.schemas.context import ContextRequest, ContextResponse
from app.services.context_service import get_context_payload

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.post('/get', response_model=ContextResponse)
def get_context(payload: ContextRequest, db: Session = Depends(db_session)):
    return get_context_payload(db, payload.query, payload.owner_id, payload.mode, payload.role)
