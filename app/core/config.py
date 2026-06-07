from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Perfume Recognition API"
    API_V1_STR: str = "/api/v1"
    
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    
    AI_PROVIDER: str = "openrouter" 
    AI_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True
    )

settings = Settings()