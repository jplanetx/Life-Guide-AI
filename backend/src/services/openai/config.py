from pydantic import BaseSettings
from functools import lru_cache

class OpenAISettings(BaseSettings):
    """OpenAI API configuration settings"""
    api_key: str
    max_retries: int = 3
    timeout: int = 30
    rate_limit_rpm: int = 50

    class Config:
        env_prefix = "OPENAI_"
        env_file = ".env"

@lru_cache()
def get_openai_settings() -> OpenAISettings:
    """Get cached OpenAI settings"""
    return OpenAISettings()