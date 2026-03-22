from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.db.models.common import CoreFields

class Assumption(CoreFields, Base):
    __tablename__ = "assumptions"
    falsification_signal: Mapped[str | None] = mapped_column(String(500), nullable=True)
    affected_items: Mapped[str | None] = mapped_column(String(1000), nullable=True)
