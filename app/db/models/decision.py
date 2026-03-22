from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.db.models.common import CoreFields

class Decision(CoreFields, Base):
    __tablename__ = "decisions"
    decision_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
    rationale: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    impact_scope: Mapped[str | None] = mapped_column(String(255), nullable=True)
