"""
Application Configuration

Centralized configuration management using environment variables
with sensible defaults and validation.
"""

import os
from typing import List, Optional
from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    
    Uses Pydantic for validation and type conversion.
    """
    
    # Application settings
    APP_NAME: str = "Ornakala Backend"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database settings
    DATABASE_URL: str = "sqlite+aiosqlite:///./ornakala.db"
    DATABASE_ECHO: bool = False
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 60
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Email settings (for future implementation)
    EMAIL_ENABLED: bool = False
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: Optional[str] = None
    
    # Redis settings (for future caching/sessions)
    REDIS_URL: Optional[str] = None
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if v == "your-secret-key-change-in-production":
            if os.getenv("ENVIRONMENT") == "production":
                raise ValueError("Secret key must be changed in production")
        return v
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            if v == "*":
                return ["*"]
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @property
    def cors_origins(self) -> List[str]:
        """Get CORS origins as a list for FastAPI CORSMiddleware"""
        return self.ALLOWED_ORIGINS
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()