from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import resolve_context_owner
from app.auth.owners import OwnerContext
from app.dependencies import require_api_key, db_session
from app.schemas.context import ContextRequest, ContextResponse
from app.services.context_service import get_context_payload

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.post('/get', response_model=ContextResponse)
def get_context(
    payload: ContextRequest,
    owner_context: OwnerContext = Depends(resolve_context_owner),
    db: Session = Depends(db_session),
):
    return get_context_payload(db, payload.query, owner_context.owner_id, payload.mode, payload.role)
