from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SkunkScrape API"
    api_v1_prefix: str = ""
    secret_key: str = "change-this-to-a-long-random-secret"
    access_token_expire_minutes: int = 1440
    cors_origins: list[str] = [
        "https://skunkscrape.com",
        "https://www.skunkscrape.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    database_url: str = "sqlite:///./skunkscrape_api.db"

    bootstrap_admin_username: str = "admin"
    bootstrap_admin_password: str = "change-me-now"
    bootstrap_admin_email: str = "admin@skunkscrape.com"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
