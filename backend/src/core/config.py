from pydantic_settings import BaseSettings
from pydantic import validator

class Settings(BaseSettings):
    # API Keys
    NOTION_API_KEY: str
    OPENAI_API_KEY: str

    # Database IDs
    NOTION_TASKS_DATABASE_ID: str
    NOTION_AREAS_DATABASE_ID: str
    NOTION_PROJECTS_DATABASE_ID: str
    NOTION_INSIGHTS_DATABASE_ID: str
    NOTION_GOALS_DATABASE_ID: str

    # Environment-specific settings
    environment: str = "development"
    debug: bool = True

    @validator("NOTION_API_KEY")
    def validate_notion_key(cls, v):
        if not v.startswith("ntn_"):
            raise ValueError("Invalid Notion API key format")
        return v

    @validator("OPENAI_API_KEY")
    def validate_openai_key(cls, v):
        if not v.startswith(("sk-", "sk-org-")):
            raise ValueError("Invalid OpenAI API key format")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True