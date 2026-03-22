from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import require_api_key, db_session
from app.schemas.goal import GoalCreate, GoalResponse
from app.services.goal_service import create_goal as service_create_goal

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.post("", response_model=GoalResponse)
def create_goal(payload: GoalCreate, db: Session = Depends(db_session)):
    return service_create_goal(db, payload)
