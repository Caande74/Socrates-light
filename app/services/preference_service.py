from sqlalchemy.orm import Session
from app.db.repositories.preferences import create_preference as repo_create_preference
from app.schemas.preference import PreferenceCreate


def create_preference(db: Session, payload: PreferenceCreate):
    data = payload.model_dump()
    return repo_create_preference(db, data)
