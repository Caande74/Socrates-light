from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from app.config import settings


def _sqlite_database_path(database_url: str) -> Path | None:
    if not database_url.startswith("sqlite:///") or database_url == "sqlite:///:memory:":
        return None
    return Path(database_url.removeprefix("sqlite:///"))


database_path = _sqlite_database_path(settings.database_url)
if database_path is not None:
    database_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(settings.database_url, future=True)


@event.listens_for(engine, "connect")
def configure_sqlite_connection(dbapi_connection, connection_record) -> None:
    if not settings.database_url.startswith("sqlite:///"):
        return

    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=FULL")
    cursor.close()


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
