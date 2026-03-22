from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.db.models.common import CoreFields

class Feedback(CoreFields, Base):
    __tablename__ = "feedback"
    target_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    target_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    signal: Mapped[str | None] = mapped_column(String(255), nullable=True)
    severity: Mapped[str | None] = mapped_column(String(50), nullable=True)
