from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Core settings
    database_url: str 
    jwt_secret: str 
    jwt_expires_minutes: int 
    app_debug: bool 
    algorithm: str

    # As requested: nested Config class (legacy-style; harmless in Pydantic v2)
    class Config:
        env_file = ".env"
        case_sensitive = False

# Singleton
settings = Settings()
