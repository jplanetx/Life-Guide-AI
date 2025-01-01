from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional
import logging

logger = logging.getLogger(__name__)

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
    NOTION_PARENT_PAGE_ID: Optional[str] = None

    # Environment-specific settings
    environment: str = "development"
    debug: bool = True

    @field_validator("NOTION_API_KEY")
    @classmethod
    def validate_notion_key(cls, v: str) -> str:
        if not v or not isinstance(v, str):
            raise ValueError("Notion API key is required")
        if not v.startswith("ntn_"):
            raise ValueError("Invalid Notion API key format - should start with 'ntn_'")
        return v

    @field_validator("OPENAI_API_KEY")
    @classmethod
    def validate_openai_key(cls, v: str) -> str:
        if not v or not isinstance(v, str):
            raise ValueError("OpenAI API key is required")
        if not v.startswith(("sk-", "sk-org-")):
            raise ValueError("Invalid OpenAI API key format - should start with 'sk-' or 'sk-org-'")
        return v

    @field_validator("NOTION_TASKS_DATABASE_ID", "NOTION_AREAS_DATABASE_ID",
                    "NOTION_PROJECTS_DATABASE_ID", "NOTION_INSIGHTS_DATABASE_ID",
                    "NOTION_GOALS_DATABASE_ID")
    @classmethod
    def validate_database_ids(cls, v: str) -> str:
        if not v or not isinstance(v, str):
            raise ValueError("Database ID is required")
        if len(v) < 32:  # Notion database IDs are typically longer
            raise ValueError("Database ID appears to be invalid (too short)")
        return v

    def validate_all(self):
        """Validate all settings at once and log their status."""
        logger.info("Validating environment variables...")

        # Check all required variables are present and correctly formatted
        required_vars = {
            "NOTION_API_KEY": "Notion API key",
            "OPENAI_API_KEY": "OpenAI API key",
            "NOTION_TASKS_DATABASE_ID": "Tasks database ID",
            "NOTION_AREAS_DATABASE_ID": "Areas database ID",
            "NOTION_PROJECTS_DATABASE_ID": "Projects database ID",
            "NOTION_INSIGHTS_DATABASE_ID": "Insights database ID",
            "NOTION_GOALS_DATABASE_ID": "Goals database ID"
        }

        for var_name, description in required_vars.items():
            value = getattr(self, var_name)
            if value:
                logger.info(f"✓ {description} is configured")
            else:
                logger.error(f"✗ {description} is missing")
                raise ValueError(f"Missing required environment variable: {var_name}")

        # Log optional variables
        optionals = ["NOTION_PARENT_PAGE_ID"]
        for var_name in optionals:
            value = getattr(self, var_name)
            if value:
                logger.info(f"✓ Optional {var_name} is configured")
            else:
                logger.info(f"○ Optional {var_name} is not configured")

        logger.info("Environment validation completed successfully")

    class Config:
        env_file = ".env"
        case_sensitive = True # This ensures we use exact case matching for env vars

# Create a function to validate settings at startup
def validate_settings():
    """Validate all settings at startup."""
    try:
        settings = Settings()
        settings.validate_all()
        return settings
    except Exception as e:
        logger.error(f"Failed to validate settings: {str(e)}")
        raise
