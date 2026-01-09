# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Perfume Recognition API"
    API_V1_STR: str = "/api/v1"
    
    # Supabase (optional for MVP)
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    
    # AI Keys (optional - using free models by default)
    AI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True
    )

settings = Settings()