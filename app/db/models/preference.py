from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.db.models.common import CoreFields

class Preference(CoreFields, Base):
    __tablename__ = "preferences"
    scope: Mapped[str | None] = mapped_column(String(255), nullable=True)
