from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.db.models.common import CoreFields

class Adjustment(CoreFields, Base):
    __tablename__ = "adjustments"
    target_scope: Mapped[str | None] = mapped_column(String(100), nullable=True)
    target_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    adjustment_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    instruction_delta: Mapped[str | None] = mapped_column(String(1000), nullable=True)
