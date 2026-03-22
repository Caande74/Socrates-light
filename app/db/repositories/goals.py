from sqlalchemy.orm import Session
from app.db.models.goal import Goal


def create_goal(db: Session, payload: dict) -> Goal:
    item = Goal(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_goal(db: Session, item_id: str) -> Goal | None:
    return db.get(Goal, item_id)


def list_active_goals(db: Session) -> list[Goal]:
    return db.query(Goal).filter(Goal.status == "active").all()