from sqlalchemy.orm import Session
from app.db.models.case_outcome import CaseOutcome


def create_case_outcome(db: Session, payload: dict) -> CaseOutcome:
    item = CaseOutcome(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_case_outcome(db: Session, item_id: str) -> CaseOutcome | None:
    return db.get(CaseOutcome, item_id)


def list_active_case_outcomes(db: Session) -> list[CaseOutcome]:
    return db.query(CaseOutcome).filter(CaseOutcome.status == "active").all()