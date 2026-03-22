from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.config import settings
from app.db.session import get_db


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")


def db_session(db: Session = Depends(get_db)) -> Session:
    return db
