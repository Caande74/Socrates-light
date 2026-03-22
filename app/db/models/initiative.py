from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.db.models.common import CoreFields

class Initiative(CoreFields, Base):
    __tablename__ = "initiatives"
    objective: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    stage: Mapped[str | None] = mapped_column(String(50), nullable=True)
    next_step: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    blockers: Mapped[str | None] = mapped_column(String(1000), nullable=True)
