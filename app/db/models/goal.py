from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.db.models.common import CoreFields

class Goal(CoreFields, Base):
    __tablename__ = "goals"
    horizon: Mapped[str | None] = mapped_column(String(50), nullable=True)
