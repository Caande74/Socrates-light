from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "unified-runtime-api-v1"
    environment: str = "development"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./runtime.db"
    api_key: str = "change-me"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
