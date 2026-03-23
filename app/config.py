from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = PROJECT_ROOT / "runtime.db"


def _normalize_database_url(database_url: str) -> str:
    if not database_url.startswith("sqlite:///"):
        return database_url

    sqlite_path = database_url.removeprefix("sqlite:///")
    if sqlite_path == ":memory:":
        return database_url

    path = Path(sqlite_path)
    if not path.is_absolute():
        path = (PROJECT_ROOT / path).resolve()

    return f"sqlite:///{path}"


class Settings(BaseSettings):
    app_name: str = "unified-runtime-api-v1"
    environment: str = "development"
    log_level: str = "INFO"
    database_url: str = f"sqlite:///{DEFAULT_DB_PATH}"
    api_key: str = "change-me"
    trusted_authenticated_subject_header: str | None = None
    api_authenticated_subject: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        return _normalize_database_url(value)

    @field_validator("database_url")
    @classmethod
    def ensure_persistent_database(cls, value: str, info) -> str:
        environment = info.data.get("environment", "development")
        if environment != "testing" and value == "sqlite:///:memory:":
            raise ValueError("DATABASE_URL cannot use an in-memory SQLite database outside testing")
        return value


settings = Settings()
