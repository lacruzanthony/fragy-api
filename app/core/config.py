# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Perfume Recognition API"
    API_V1_STR: str = "/api/v1"
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # AI Keys (Gemini o OpenAI)
    AI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True
    )

settings = Settings()