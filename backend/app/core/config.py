import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Personal Finance Tracker"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "super-secret-key-for-dev-only"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    # We override this in database.py for the exe, but good to have a default
    DATABASE_URL: str = "sqlite:///./finances.db"

    # CORS (Cross-Origin Resource Sharing)
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Configuration to ignore extra fields in .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore", 
        case_sensitive=True
    )

settings = Settings()