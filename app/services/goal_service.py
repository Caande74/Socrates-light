from sqlalchemy.orm import Session
from app.db.repositories.goals import create_goal as repo_create_goal
from app.schemas.goal import GoalCreate


def create_goal(db: Session, payload: GoalCreate):
    data = payload.model_dump()
    return repo_create_goal(db, data)