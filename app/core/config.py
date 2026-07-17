from functools import lru_cache

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_name: str = "Feedback Service"
    app_env: str = "development"
    debug: bool = True
    cors_origins: str = ""

    # Database
    database_url: str

    # AI (Groq)
    groq_api_key: str
    groq_model: str = "llama-3.1-8b-instant"

    # Email (Resend)
    resend_api_key: str
    email_from: EmailStr
    owner_email: EmailStr

    # Rate limiting
    rate_limit_requests: int = 5
    rate_limit_window_seconds: int = 60

    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/app.log"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()