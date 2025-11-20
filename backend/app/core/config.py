import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Personal Finance Tracker"
    API_V1_STR: str = "/api/v1"
    
    # Provide a default secret key for the local desktop app to function out-of-the-box
    SECRET_KEY: str = os.getenv("SECRET_KEY", "local-desktop-app-fallback-key-999")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    
    PLAID_CLIENT_ID: Optional[str] = os.getenv("PLAID_CLIENT_ID")
    PLAID_SECRET: Optional[str] = os.getenv("PLAID_SECRET")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")

    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True
    )

settings = Settings()