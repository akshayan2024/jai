import os
from pathlib import Path
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application settings
    APP_NAME: str = "JAI API"
    APP_ENV: str = os.getenv("PYTHON_ENV", "development")
    DEBUG: bool = APP_ENV == "development"
    
    # Ephemeris settings
    EPHEMERIS_PATH: str = os.getenv("EPHEMERIS_PATH", "./ephemeris")
    
    # Default ayanamsa
    DEFAULT_AYANAMSA: str = "lahiri"
    
    # Deployment settings
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create global settings instance
settings = Settings() 