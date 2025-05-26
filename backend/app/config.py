from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Travel Mood API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str = "postgresql://travel_user:travel_pass@localhost:5432/travel_mood"
    REDIS_URL: str = "redis://localhost:6379"
    
    # Azure OpenAI - GPT-4o
    AZURE_OPENAI_ENDPOINT: str = "https://kcg-openai-instance.openai.azure.com/"
    AZURE_OPENAI_API_KEY: str = "873198d21c634d00931dba12f72667b2"
    AZURE_OPENAI_API_VERSION: str = "2023-05-15"
    AZURE_OPENAI_DEPLOYMENT_NAME: str = "gpt-4o"
    
    # Azure OpenAI - Embeddings
    AZURE_OPENAI_EMBEDDING_ENDPOINT: str = "https://kcg-openai-instance-japan-east.openai.azure.com/"
    AZURE_OPENAI_EMBEDDING_API_KEY: str = "268cd6b3f8734c40a90f5abba54f6bdd"
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str = "text-embedding-ada-002"
    
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    CACHE_TTL: int = 300
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
