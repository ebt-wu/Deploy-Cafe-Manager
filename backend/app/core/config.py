# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/gic"
    API_PREFIX: str = "/api" 
    CORS_ORIGINS: list[str] = []

    class Config:
        env_file = ".env"

settings = Settings()
settings.API_PREFIX = settings.API_PREFIX.rstrip("/")  # normalize
