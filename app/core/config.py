"""
Centralized application configuration.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application-wide settings."""

    DATABASE_URL: str = "sqlite:///./task_management.db"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
