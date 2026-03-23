import app.db.models
from fastapi import FastAPI
from app.api.router import api_router
from app.auth.middleware import attach_authenticated_subject
from app.config import settings
from app.logging import configure_logging
from app.db.base import Base
from app.db.session import engine

configure_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="0.1.0")
app.middleware("http")(attach_authenticated_subject)
app.include_router(api_router)
