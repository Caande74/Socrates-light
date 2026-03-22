from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.db.models.common import CoreFields

class Pattern(CoreFields, Base):
    __tablename__ = "patterns"
    pattern_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
