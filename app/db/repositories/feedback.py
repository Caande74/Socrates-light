from sqlalchemy.orm import Session
from app.db.models.feedback import Feedback


def find_active_feedback_by_content(db: Session, content: str, owner_id: str) -> Feedback | None:
    return (
        db.query(Feedback)
        .filter(
            Feedback.status == "active",
            Feedback.content == content,
            Feedback.owner_id == owner_id,
        )
        .first()
    )


def create_feedback(db: Session, payload: dict) -> Feedback:
    item = Feedback(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_feedback(db: Session, item_id: str) -> Feedback | None:
    return db.get(Feedback, item_id)


def list_active_feedback(db: Session, owner_id: str | None = None) -> list[Feedback]:
    query = db.query(Feedback).filter(Feedback.status == "active")
    if owner_id is not None:
        query = query.filter(Feedback.owner_id == owner_id)
    return query.all()
