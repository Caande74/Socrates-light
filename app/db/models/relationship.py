from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Relationship(Base):
    __tablename__ = "relationships"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    from_type: Mapped[str] = mapped_column(String(50))
    from_id: Mapped[str] = mapped_column(String(64))
    to_type: Mapped[str] = mapped_column(String(50))
    to_id: Mapped[str] = mapped_column(String(64))
    relationship_type: Mapped[str] = mapped_column(String(100))
