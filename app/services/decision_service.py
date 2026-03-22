from sqlalchemy.orm import Session
from app.db.repositories.decisions import create_decision as repo_create_decision
from app.schemas.decision import DecisionCreate


def create_decision(db: Session, payload: DecisionCreate):
    data = payload.model_dump()
    return repo_create_decision(db, data)
